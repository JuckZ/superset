# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file to
# you under the Apache License, Version 2.0 (the
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
import json
import logging
from typing import Any

import lark_oapi as lark
from flask import current_app
from lark_oapi.api.im.v1 import CreateImageRequest, CreateImageRequestBody

from superset.reports.models import ReportRecipientType
from superset.reports.notifications.base import BaseNotification
from superset.reports.notifications.exceptions import NotificationError
from superset.utils.decorators import statsd_gauge

logger = logging.getLogger(__name__)


class LarkAppNotification(BaseNotification):
    """
    Sends notifications via Lark (Feishu) App using batch message API.
    Supports sending to both users and group chats.
    """

    type = ReportRecipientType.LARK_APP

    def _get_lark_client(self) -> lark.Client:
        """
        Get Lark client using app_id and app_secret from config.
        :returns: Lark client instance
        :raises NotificationError: If credentials are not configured
        """
        app_id = current_app.config.get("LARK_APP_ID")
        app_secret = current_app.config.get("LARK_APP_SECRET")

        if not app_id or not app_secret:
            raise NotificationError(
                "Lark App credentials not configured. "
                "Please set LARK_APP_ID and LARK_APP_SECRET in config."
            )

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
            raise NotificationError(f"Error creating Lark client: {ex}") from ex

    def _upload_image(self, image_bytes: bytes, client: lark.Client) -> str | None:
        """
        Upload image to Lark and get image_key.
        Reference: https://open.feishu.cn/document/server-docs/im-v1/image/create
        :param image_bytes: Image bytes to upload
        :param client: Lark client instance
        :returns: Image key if successful, None otherwise
        """
        try:
            image_file = io.BytesIO(image_bytes)
            request_body = (
                CreateImageRequestBody.builder()
                .image_type("message")
                .image(image_file)
                .build()
            )
            request = CreateImageRequest.builder().request_body(request_body).build()
            response = client.im.v1.image.create(request)

            if response.code == 0:
                image_key = response.data.image_key if response.data else None
                if image_key:
                    logger.debug("Successfully uploaded image, image_key: %s", image_key)
                    return image_key
                logger.warning("Image upload succeeded but no image_key returned")
                return None

            logger.warning(
                "Failed to upload image: code=%s, msg=%s",
                response.code,
                response.msg,
            )
            return None
        except Exception as ex:
            logger.warning("Error uploading image to Lark: %s", str(ex))
            return None

    def _build_message_card(self) -> dict[str, Any]:
        """
        Build interactive card message content.
        Reference: https://open.feishu.cn/document/server-docs/im-v1/message-content-description/card
        :returns: Message card structure
        """
        client = self._get_lark_client()

        # Build markdown content
        markdown_parts = []
        if self._content.description:
            markdown_parts.append(f"**描述**: {self._content.description}")
        if self._content.header_data.get("notification_type"):
            markdown_parts.append(
                f"**类型**: {self._content.header_data.get('notification_type')}"
            )
        if self._content.header_data.get("notification_format"):
            markdown_parts.append(
                f"**格式**: {self._content.header_data.get('notification_format')}"
            )
        if self._content.text:
            markdown_parts.append(f"\n{self._content.text}")

        markdown_content = (
            "\n".join(markdown_parts) if markdown_parts else "Superset 告警通知"
        )

        # Build card elements
        elements = [
            {
                "tag": "markdown",
                "content": markdown_content,
            }
        ]

        # Add images if screenshots are available
        if self._content.screenshots:
            for screenshot in self._content.screenshots:
                image_key = self._upload_image(screenshot, client)
                if image_key:
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

        # Build card structure
        subject = self._content.name if self._content.name else "Superset 告警通知"

        card = {
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
                        "content": "点击标题跳转到报表地址",
                    },
                },
            },
        }

        # Add card_link if URL is available
        if self._content.url:
            card["card"]["card_link"] = {
                "url": self._content.url,
            }

        return card

    def _parse_recipients(self) -> dict[str, list[str]]:
        """
        Parse recipient configuration to extract recipients by ID type.
        Expected format in recipient_config_json:
        {
            "open_id": ["ou_xxx", "ou_yyy"],
            "user_id": ["12345", "67890"],
            "union_id": ["on_xxx"],
            "email": ["user@example.com"],
            "chat_id": ["oc_xxx", "oc_yyy"]
        }
        The keys represent the receive_id_type, and values are lists of IDs.
        :returns: Dictionary mapping receive_id_type to list of IDs
        :raises NotificationError: If configuration is invalid
        """
        valid_id_types = {"open_id", "user_id", "union_id", "email", "chat_id"}
        
        try:
            config = json.loads(self._recipient.recipient_config_json)
            
            # If the config is wrapped in "target" (frontend's standard storage), unwrap it
            actual_config = config
            if isinstance(config, dict) and "target" in config:
                target_value = config["target"]
                try:
                    # Try to parse target as JSON if it's a string
                    if isinstance(target_value, str):
                        actual_config = json.loads(target_value)
                    else:
                        actual_config = target_value
                except (json.JSONDecodeError, TypeError):
                    # If it's not JSON, assume it's direct config (unlikely but possible)
                    actual_config = config

            recipients: dict[str, list[str]] = {}
            
            for id_type, ids in actual_config.items():
                if id_type not in valid_id_types:
                    # Skip 'target' if it was part of the original wrapper but didn't contain JSON
                    if id_type == "target":
                        continue
                    
                    logger.warning(
                        "Invalid receive_id_type '%s', skipping. "
                        "Valid types: %s",
                        id_type,
                        valid_id_types,
                    )
                    continue
                
                if not isinstance(ids, list):
                    logger.warning(
                        "Value for '%s' must be a list, got %s, skipping",
                        id_type,
                        type(ids).__name__,
                    )
                    continue
                
                if ids:  # Only add non-empty lists
                    recipients[id_type] = ids
            
            if not recipients:
                raise NotificationError(
                    "No valid recipients configured. Please specify at least one of: "
                    f"{', '.join(valid_id_types)}"
                )
            
            return recipients
        except json.JSONDecodeError as ex:
            raise NotificationError("Invalid recipient configuration JSON") from ex

    @statsd_gauge("reports.lark_app.send")
    def send(self) -> None:
        """
        Send notification to Lark App recipients.
        Supports multiple ID types: open_id, user_id, union_id, email, chat_id.
        Reference: https://open.feishu.cn/document/server-docs/im-v1/message/create
        """
        client = self._get_lark_client()
        recipients_by_type = self._parse_recipients()

        # Build message content
        message_card = self._build_message_card()
        message_content = json.dumps(message_card["card"])

        # Send to each recipient type
        for receive_id_type, recipient_ids in recipients_by_type.items():
            for recipient_id in recipient_ids:
                try:
                    from lark_oapi.api.im.v1 import (
                        CreateMessageRequest,
                        CreateMessageRequestBody,
                    )

                    request_body = (
                        CreateMessageRequestBody.builder()
                        .receive_id(recipient_id)
                        .msg_type("interactive")
                        .content(message_content)
                        .build()
                    )
                    request = (
                        CreateMessageRequest.builder()
                        .receive_id_type(receive_id_type)
                        .request_body(request_body)
                        .build()
                    )

                    response = client.im.v1.message.create(request)

                    if response.code != 0:
                        logger.error(
                            "Failed to send message to %s '%s': code=%s, msg=%s",
                            receive_id_type,
                            recipient_id,
                            response.code,
                            response.msg,
                        )
                        raise NotificationError(
                            f"Failed to send message to {receive_id_type} '{recipient_id}': "
                            f"code={response.code}, msg={response.msg}"
                        )

                    logger.info(
                        "Successfully sent Lark App notification to %s '%s'",
                        receive_id_type,
                        recipient_id,
                    )
                except NotificationError:
                    raise
                except Exception as ex:
                    raise NotificationError(
                        f"Error sending message to {receive_id_type} '{recipient_id}': {ex}"
                    ) from ex
