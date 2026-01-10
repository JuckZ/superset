# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import io
import logging
from typing import Any, Optional
from urllib.parse import urlparse

import backoff
import lark_oapi as lark
import pandas as pd
import requests
from flask import current_app
from lark_oapi.api.im.v1 import (
    CreateFileRequest,
    CreateFileRequestBody,
    CreateImageRequest,
    CreateImageRequestBody,
)

from superset import feature_flag_manager
from superset.reports.models import ReportRecipientType
from superset.reports.notifications.base import BaseNotification
from superset.reports.notifications.exceptions import (
    NotificationParamException,
    NotificationUnprocessableException,
)
from superset.utils import json
from superset.utils.decorators import statsd_gauge

logger = logging.getLogger(__name__)


class WebhookNotification(BaseNotification):
    """
    Sends a post request to a webhook url
    """

    type = ReportRecipientType.WEBHOOK

    def _get_webhook_url(self) -> str:
        """
        Get the webhook URL from the recipient configuration
        :returns: The webhook URL
        :raises NotificationParamException: If the webhook URL is not provided in the recipient configuration
        """  # noqa: E501
        try:
            cfg = json.loads(self._recipient.recipient_config_json)
            target = cfg.get("target") if isinstance(cfg, dict) else None
            if not target:
                raise NotificationParamException("Webhook URL is required")
            return target
        except (json.JSONDecodeError, KeyError, TypeError) as ex:
            raise NotificationParamException("Webhook URL is required") from ex

    def _is_feishu_webhook(self) -> bool:
        """
        Check if the webhook URL is a Feishu webhook
        :returns: True if the webhook URL is a Feishu webhook, False otherwise
        """
        try:
            wh_url = self._get_webhook_url()
            parsed_url = urlparse(wh_url)
            return "open.feishu.cn" in parsed_url.netloc.lower()
        except NotificationParamException:
            return False

    def _get_feishu_client(self) -> Optional[lark.Client]:
        """
        Get Feishu client using app_id and app_secret
        Reference: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM
        :returns: Lark client if configured, None otherwise
        """
        app_id = current_app.config.get("LARK_APP_ID")
        app_secret = current_app.config.get("LARK_APP_SECRET")

        if not app_id or not app_secret:
            logger.debug("Feishu app_id or app_secret not configured, skipping image upload")
            return None

        try:
            client = (
                lark.Client.builder()
                .app_id(app_id)
                .app_secret(app_secret)
                .log_level(lark.LogLevel.ERROR)
                .build()
            )
            return client
        except Exception as ex:
            logger.warning("Error creating Feishu client: %s", str(ex))
            return None

    def _upload_feishu_image(self, image_bytes: bytes, client: lark.Client) -> Optional[str]:
        """
        Upload image to Feishu and get image_key using lark_oapi
        Reference: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
        :param image_bytes: Image bytes to upload
        :param client: Lark client instance
        :returns: Image key if successful, None otherwise
        """
        try:
            # Convert bytes to file-like object as required by Feishu API
            image_file = io.BytesIO(image_bytes)
            
            # Create request body
            request_body = (
                CreateImageRequestBody.builder()
                .image_type("message")
                .image(image_file)
                .build()
            )

            # Create request
            request = CreateImageRequest.builder().request_body(request_body).build()

            # Call API
            response = client.im.v1.image.create(request)

            if response.code == 0:
                image_key = response.data.image_key if response.data else None
                if image_key:
                    logger.debug("Successfully uploaded image to Feishu, image_key: %s", image_key)
                    return image_key
                else:
                    logger.warning("Feishu image upload succeeded but no image_key returned")
                    return None
            else:
                logger.warning(
                    "Failed to upload image to Feishu: code=%s, msg=%s",
                    response.code,
                    response.msg,
                )
                return None
        except Exception as ex:
            logger.warning("Error uploading image to Feishu: %s", str(ex))
            return None

    def _upload_feishu_file(
        self, file_bytes: bytes, filename: str, client: lark.Client
    ) -> Optional[str]:
        """
        Upload file to Feishu and get file_key using lark_oapi
        Reference: https://open.feishu.cn/document/server-docs/im-v1/file/create
        :param file_bytes: File bytes to upload
        :param filename: File name to use in Feishu
        :param client: Lark client instance
        :returns: File key if successful, None otherwise
        """
        try:
            file_obj = io.BytesIO(file_bytes)
            request_body = (
                CreateFileRequestBody.builder()
                .file_type("pdf")
                .file_name(filename)
                .file(file_obj)
                .build()
            )
            request = CreateFileRequest.builder().request_body(request_body).build()
            response = client.im.v1.file.create(request)

            if response.code == 0:
                file_key = response.data.file_key if response.data else None
                if file_key:
                    logger.debug("Successfully uploaded file to Feishu, file_key: %s", file_key)
                    return file_key
                logger.warning("Feishu file upload succeeded but no file_key returned")
                return None

            logger.warning(
                "Failed to upload file to Feishu: code=%s, msg=%s",
                response.code,
                response.msg,
            )
            return None
        except Exception as ex:
            logger.warning("Error uploading file to Feishu: %s", str(ex))
            return None

    def _csv_to_markdown_table(self, csv_bytes: bytes, max_rows: int = 50) -> Optional[str]:
        """
        Convert CSV bytes to markdown table format
        :param csv_bytes: CSV file bytes
        :param max_rows: Maximum number of rows to include in the table
        :returns: Markdown table string if successful, None otherwise
        """
        try:
            # Read CSV into DataFrame
            df = pd.read_csv(io.BytesIO(csv_bytes))

            # Check if DataFrame is empty
            if df.empty:
                logger.debug("CSV data is empty, skipping markdown table conversion")
                return None

            # Fill NaN values with empty string for better display
            df = df.fillna("")

            # Limit rows to avoid message size limits
            original_row_count = len(df)
            if original_row_count > max_rows:
                df = df.head(max_rows)
                logger.info(
                    "CSV has %d rows, limiting to %d rows for markdown table",
                    original_row_count,
                    max_rows,
                )

            # Convert DataFrame to markdown table
            # Use index=False to exclude index column, tablefmt="pipe" for pipe tables
            markdown_table = df.to_markdown(index=False, tablefmt="pipe")

            # Add truncation notice if rows were limited
            if original_row_count > max_rows:
                markdown_table += f"\n\n*(表格已截断，共 {original_row_count} 行，仅显示前 {max_rows} 行)*"

            return markdown_table
        except Exception as ex:
            logger.warning("Error converting CSV to markdown table: %s", str(ex))
            return None

    def _get_feishu_payload(self) -> dict[str, Any]:
        """
        Get the payload formatted for Feishu webhook API with interactive card
        Reference: https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
        :returns: Feishu-formatted payload dictionary with card structure
        """
        # Build markdown content from notification data
        markdown_parts = []
        if self._content.description:
            markdown_parts.append(f"**描述**: {self._content.description}")

        if self._content.header_data.get("chart_id"):
            markdown_parts.append(
                f"**图表ID**: {self._content.header_data.get('chart_id')}"
            )
        if self._content.header_data.get("dashboard_id"):
            markdown_parts.append(
                f"**仪表板ID**: {self._content.header_data.get('dashboard_id')}"
            )
        if self._content.text:
            markdown_parts.append(f"\n{self._content.text}")

        # Add CSV data as markdown table if available
        if self._content.csv:
            csv_table = self._csv_to_markdown_table(self._content.csv)
            if csv_table:
                markdown_parts.append("\n**数据表格**:\n")
                markdown_parts.append(csv_table)

        markdown_content = "\n".join(markdown_parts) if markdown_parts else "Superset 告警通知"

        # Use name as subject, fallback to default if not available
        subject = self._content.name if self._content.name else "Superset 告警通知"

        # Build card structure
        elements = [
            {
                "tag": "markdown",
                "content": markdown_content,
            }
        ]

        client = None
        if self._content.screenshots:
            client = self._get_feishu_client()
            if not client:
                logger.warning(
                    "Feishu client not available, skipping image uploads. "
                    "Please configure LARK_APP_ID and LARK_APP_SECRET."
                )

        # Add images if screenshots are available
        if self._content.screenshots and client:
            for screenshot in self._content.screenshots:
                image_key = self._upload_feishu_image(screenshot, client)
                if image_key:
                    # Add image element to card
                    elements.append(
                        {
                            "tag": "img",
                            "img_key": image_key,
                            "alt": {
                                "tag": "plain_text",
                                "content": "报表截图",
                            },
                        }
                    )

        payload: dict[str, Any] = {
            "msg_type": "interactive",
            "card": {
                "schema": "2.0",
                "config": {
                    "enable_forward": True,
                    "update_multi": True,
                },
                "body": {
                    "direction": "vertical",
                    "elements": elements,
                },
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": subject,
                    },
                    "subtitle": {
                        "tag": "plain_text",
                        "content": "点击跳转到报表地址",
                    },
                },
            },
        }

        # Add card_link if URL is available
        if self._content.url:
            payload["card"]["card_link"] = {
                "url": self._content.url,
            }

        return payload

    def _get_feishu_file_payload(self, file_key: str, file_name: str) -> dict[str, Any]:
        """
        Get the payload formatted for Feishu webhook API file message
        :param file_key: Feishu file_key from upload
        :param file_name: File name to show in message
        :returns: Feishu-formatted payload dictionary for file message
        """
        return {
            "msg_type": "file",
            "content": {
                "file_key": file_key,
            },
        }

    def _get_req_payload(self) -> dict[str, Any]:
        """
        Get the request payload for the webhook
        Returns Feishu-formatted payload if the webhook URL is a Feishu webhook,
        otherwise returns the default format for backward compatibility
        :returns: Payload dictionary
        """
        if self._is_feishu_webhook():
            return self._get_feishu_payload()

        header_content = {
            "chart_id": self._content.header_data.get("chart_id"),
            "dashboard_id": self._content.header_data.get("dashboard_id"),
        }
        content = {
            "name": self._content.name,
            "header": header_content,
            "text": self._content.text,
            "description": self._content.description,
            "url": self._content.url,
        }
        return content

    def _get_files(self) -> list[tuple[str, tuple[str, bytes, str]]]:
        files = []
        if self._content.csv:
            files.append(("files", ("report.csv", self._content.csv, "text/csv")))
        if self._content.pdf:
            files.append(
                ("files", ("report.pdf", self._content.pdf, "application/pdf"))
            )
        if self._content.screenshots:
            for i, screenshot in enumerate(self._content.screenshots):
                files.append(
                    (
                        "files",
                        (f"screenshot_{i}.png", screenshot, "image/png"),
                    )
                )
        return files

    @backoff.on_exception(
        backoff.expo, NotificationUnprocessableException, factor=10, base=2, max_tries=5
    )
    @statsd_gauge("reports.webhook.send")
    def send(self) -> None:
        if not feature_flag_manager.is_feature_enabled("ALERT_REPORT_WEBHOOK"):
            raise NotificationUnprocessableException(
                "Attempted to send a Webhook notification but Webhook feature flag \
                is not enabled."
            )
        wh_url = self._get_webhook_url()
        if current_app.config["ALERT_REPORTS_WEBHOOK_HTTPS_ONLY"]:
            if urlparse(wh_url).scheme.lower() != "https":
                raise NotificationParamException(
                    "Webhook failed: HTTPS is required by config for webhook URLs."
                )
        payload = self._get_req_payload()
        files = self._get_files()
        is_feishu = self._is_feishu_webhook()

        # Log request details, especially for Feishu webhooks
        if is_feishu:
            logger.info("=" * 80)
            logger.info("Feishu Webhook Request Details")
            logger.info("=" * 80)
            logger.info("URL: %s", wh_url)
            logger.info("Payload: %s", json.dumps(payload, indent=2))
            logger.info("Files: %s", f"{len(files)} file(s)" if files else "No files")
            logger.info("=" * 80)
        else:
            logger.debug("Sending webhook request to %s", wh_url)
            logger.debug("Payload: %s", json.dumps(payload))

        try:
            # Feishu webhook API only supports JSON payload, not multipart/form-data
            # So we skip file attachments for Feishu webhooks
            if files and not is_feishu:
                data = {}
                for key, value in payload.items():
                    if isinstance(value, (dict, list)):
                        data[key] = json.dumps(value)
                    else:
                        data[key] = value

                response = requests.post(wh_url, data=data, files=files, timeout=60)
            else:
                # For Feishu webhooks or webhooks without files, use JSON payload
                response = requests.post(wh_url, json=payload, timeout=60)

            # Log response details, especially for Feishu webhooks
            if is_feishu:
                logger.info("=" * 80)
                logger.info("Feishu Webhook Response Details")
                logger.info("=" * 80)
                logger.info("Status Code: %s", response.status_code)
                logger.info("Status Text: %s", response.reason)
                logger.info("Response Headers: %s", json.dumps(dict(response.headers), indent=2))
                logger.info("Response Body (Text): %s", response.text)
                # Try to parse JSON response for better logging
                try:
                    response_json = response.json()
                    logger.info("Response Body (JSON): %s", json.dumps(response_json, indent=2))
                    # Log Feishu-specific response code if present
                    if isinstance(response_json, dict) and "code" in response_json:
                        logger.info("Feishu Response Code: %s", response_json.get("code"))
                        logger.info("Feishu Response Message: %s", response_json.get("msg", "N/A"))
                except (ValueError, TypeError):
                    logger.info("Response is not valid JSON")
                logger.info("=" * 80)
            else:
                logger.info(
                    "Webhook sent to %s, status code: %s", wh_url, response.status_code
                )

            if response.status_code >= 500 or response.status_code == 429:
                raise NotificationUnprocessableException(
                    f"Webhook failed with status code {response.status_code}: \
                     {response.text}"
                )
            if response.status_code >= 400:
                raise NotificationParamException(
                    f"Webhook failed with status code {response.status_code}: \
                    {response.text}"
                )

            if is_feishu and self._content.pdf:
                client = self._get_feishu_client()
                if not client:
                    logger.warning(
                        "Feishu client not available, skipping PDF upload. "
                        "Please configure LARK_APP_ID and LARK_APP_SECRET."
                    )
                    return

                file_key = self._upload_feishu_file(self._content.pdf, "report.pdf", client)
                if not file_key:
                    logger.warning("Failed to upload PDF to Feishu, skipping file message")
                    return

                file_payload = self._get_feishu_file_payload(file_key, "report.pdf")
                file_response = requests.post(wh_url, json=file_payload, timeout=60)

                logger.info("=" * 80)
                logger.info("Feishu Webhook File Response Details")
                logger.info("=" * 80)
                logger.info("Status Code: %s", file_response.status_code)
                logger.info("Status Text: %s", file_response.reason)
                logger.info(
                    "Response Headers: %s",
                    json.dumps(dict(file_response.headers), indent=2),
                )
                logger.info("Response Body (Text): %s", file_response.text)
                try:
                    file_response_json = file_response.json()
                    logger.info(
                        "Response Body (JSON): %s",
                        json.dumps(file_response_json, indent=2),
                    )
                    if isinstance(file_response_json, dict) and "code" in file_response_json:
                        logger.info(
                            "Feishu Response Code: %s", file_response_json.get("code")
                        )
                        logger.info(
                            "Feishu Response Message: %s",
                            file_response_json.get("msg", "N/A"),
                        )
                except (ValueError, TypeError):
                    logger.info("Response is not valid JSON")
                logger.info("=" * 80)

                if file_response.status_code >= 500 or file_response.status_code == 429:
                    raise NotificationUnprocessableException(
                        f"Webhook failed with status code {file_response.status_code}: \
                         {file_response.text}"
                    )
                if file_response.status_code >= 400:
                    raise NotificationParamException(
                        f"Webhook failed with status code {file_response.status_code}: \
                        {file_response.text}"
                    )

        except requests.exceptions.RequestException as ex:
            raise NotificationUnprocessableException(str(ex)) from ex
