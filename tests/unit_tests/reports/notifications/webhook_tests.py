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
import os
from typing import Optional

import pandas as pd
import pytest
from PIL import Image

from superset.reports.notifications.exceptions import (
    NotificationParamException,
)
from superset.reports.notifications.webhook import WebhookNotification
from superset.utils.core import HeaderDataType


@pytest.fixture
def mock_header_data() -> HeaderDataType:
    return {
        "notification_format": "PNG",
        "notification_type": "Alert",
        "owners": [1],
        "notification_source": None,
        "chart_id": None,
        "dashboard_id": None,
        "slack_channels": None,
        "execution_id": "test-execution-id",
    }


def test_get_webhook_url(mock_header_data) -> None:
    """
    Test the _get_webhook_url function to ensure it correctly extracts
    the webhook URL from recipient configuration
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    content = NotificationContent(
        name="test alert",
        header_data=mock_header_data,
        embedded_data=pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}),
        description="Test description",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "https://example.com/webhook"}',
        ),
        content=content,
    )

    result = webhook_notification._get_webhook_url()

    assert result == "https://example.com/webhook"


def test_get_webhook_url_missing_url(mock_header_data) -> None:
    """
    Test that _get_webhook_url raises an exception when URL is missing
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    content = NotificationContent(
        name="test alert",
        header_data=mock_header_data,
        description="Test description",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json="{}",
        ),
        content=content,
    )

    with pytest.raises(NotificationParamException, match="Webhook URL is required"):
        webhook_notification._get_webhook_url()


def test_get_req_payload_basic(mock_header_data) -> None:
    """
    Test that _get_req_payload returns correct payload structure
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    content = NotificationContent(
        name="Payload Name",
        header_data=mock_header_data,
        embedded_data=None,
        description="Payload Description",
        url="http://example.com/report",
        text="Report Text",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "https://webhook.com"}',
        ),
        content=content,
    )

    payload = webhook_notification._get_req_payload()

    assert payload["name"] == "Payload Name"
    assert payload["description"] == "Payload Description"
    assert payload["url"] == "http://example.com/report"
    assert payload["text"] == "Report Text"
    assert isinstance(payload["header"], dict)
    # Optional fields from header_data
    assert payload["header"]["notification_format"] == "PNG"
    assert payload["header"]["notification_type"] == "Alert"


def test_get_files_includes_all_content_types(mock_header_data) -> None:
    """
    Test that _get_files correctly includes csv, pdf, and multiple screenshot attachments
    """  # noqa: E501

    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    csv_bytes = b"col1,col2\n1,2"
    pdf_bytes = b"%PDF-1.4"
    screenshots = [b"fakeimg1", b"fakeimg2"]

    content = NotificationContent(
        name="file test",
        header_data=mock_header_data,
        csv=csv_bytes,
        pdf=pdf_bytes,
        screenshots=screenshots,
        description="files test",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "https://webhook.com"}',
        ),
        content=content,
    )
    files = webhook_notification._get_files()
    # There should be 1 csv, 1 pdf, and 2 screenshots = 4 files total
    assert len(files) == 4

    file_names = [file_info[1][0] for file_info in files]
    assert "report.csv" in file_names
    assert "report.pdf" in file_names
    assert "screenshot_0.png" in file_names
    assert "screenshot_1.png" in file_names

    mime_types = [file_info[1][2] for file_info in files]
    assert "text/csv" in mime_types
    assert "application/pdf" in mime_types
    assert mime_types.count("image/png") == 2


def test_get_files_empty_when_no_content(mock_header_data) -> None:
    """
    Test that _get_files returns empty list when no files present
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    content = NotificationContent(
        name="no files",
        header_data=mock_header_data,
        description="no files test",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "https://webhook.com"}',
        ),
        content=content,
    )
    files = webhook_notification._get_files()
    assert files == []


def test_get_feishu_payload_excludes_pdf(mock_header_data, monkeypatch) -> None:
    """
    Test that Feishu payload excludes PDF file elements
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    pdf_bytes = b"%PDF-1.4"
    content = NotificationContent(
        name="PDF payload",
        header_data=mock_header_data,
        description="PDF test",
        pdf=pdf_bytes,
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "https://open.feishu.cn/webhook/test"}',
        ),
        content=content,
    )

    payload = webhook_notification._get_req_payload()

    assert payload["msg_type"] == "interactive"
    elements = payload["card"]["body"]["elements"]
    assert all(element.get("tag") != "file" for element in elements)


def test_get_feishu_file_payload(mock_header_data) -> None:
    """
    Test that Feishu file payload uses msg_type file
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    content = NotificationContent(
        name="file payload",
        header_data=mock_header_data,
        description="file payload test",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "https://open.feishu.cn/webhook/test"}',
        ),
        content=content,
    )

    payload = webhook_notification._get_feishu_file_payload("file_key", "report.pdf")

    assert payload["msg_type"] == "file"
    assert payload["content"]["file_key"] == "file_key"


def test_send_http_only_https_check(monkeypatch, mock_header_data) -> None:
    """
    Test send raises when URL is not HTTPS and config enforces HTTPS only
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    content = NotificationContent(
        name="test alert", header_data=mock_header_data, description="Test description"
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json='{"target": "http://notsecure.com/webhook"}',
        ),
        content=content,
    )

    class MockCurrentApp:
        config = {"ALERT_REPORTS_WEBHOOK_HTTPS_ONLY": True}

    monkeypatch.setattr(
        "superset.reports.notifications.webhook.current_app", MockCurrentApp
    )
    monkeypatch.setattr(
        "superset.reports.notifications.webhook.feature_flag_manager.is_feature_enabled",
        lambda flag: True,
    )

    with pytest.raises(NotificationParamException, match="HTTPS is required by config"):
        webhook_notification.send()


def _create_test_image(width: int = 100, height: int = 100, color: str = "red") -> bytes:
    """
    Helper function to create test PNG image bytes
    :param width: Image width in pixels
    :param height: Image height in pixels
    :param color: Background color name
    :returns: PNG image bytes
    """
    img = Image.new("RGB", (width, height), color)
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


def _get_feishu_config() -> Optional[dict[str, str]]:
    """
    Get Feishu configuration from environment variables
    :returns: Dictionary with app_id, app_secret, and webhook_url if all are set, None otherwise
    """
    app_id = os.getenv("LARK_APP_ID")
    app_secret = os.getenv("LARK_APP_SECRET")
    webhook_url = os.getenv("FEISHU_WEBHOOK_URL")

    if app_id and app_secret and webhook_url:
        return {
            "app_id": app_id,
            "app_secret": app_secret,
            "webhook_url": webhook_url,
        }
    return None


def _has_feishu_config() -> bool:
    """
    Check if Feishu configuration is available
    :returns: True if all required environment variables are set, False otherwise
    """
    return _get_feishu_config() is not None


@pytest.mark.skipif(
    not _has_feishu_config(),
    reason="Feishu integration tests require LARK_APP_ID, LARK_APP_SECRET, and FEISHU_WEBHOOK_URL environment variables",
)
def test_upload_feishu_image_integration(mock_header_data, monkeypatch) -> None:
    """
    Integration test for _upload_feishu_image method
    Tests actual image upload to Feishu API
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    feishu_config = _get_feishu_config()
    assert feishu_config is not None

    # Create test image
    test_image_bytes = _create_test_image(200, 200, "blue")

    content = NotificationContent(
        name="test image upload",
        header_data=mock_header_data,
        description="Test Feishu image upload",
    )
    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json=f'{{"target": "{feishu_config["webhook_url"]}"}}',
        ),
        content=content,
    )

    # Mock Flask current_app config
    class MockCurrentApp:
        config = {
            "LARK_APP_ID": feishu_config["app_id"],
            "LARK_APP_SECRET": feishu_config["app_secret"],
        }

    monkeypatch.setattr(
        "superset.reports.notifications.webhook.current_app", MockCurrentApp
    )

    # Get Feishu client
    client = webhook_notification._get_feishu_client()
    assert client is not None, "Feishu client should be created with valid credentials"

    # Upload image
    image_key = webhook_notification._upload_feishu_image(test_image_bytes, client)

    # Verify upload was successful
    assert image_key is not None, "Image upload should return a valid image_key"
    assert isinstance(image_key, str), "image_key should be a string"
    assert len(image_key) > 0, "image_key should not be empty"


@pytest.mark.skipif(
    not _has_feishu_config(),
    reason="Feishu integration tests require LARK_APP_ID, LARK_APP_SECRET, and FEISHU_WEBHOOK_URL environment variables",
)
def test_send_feishu_webhook_integration(mock_header_data, monkeypatch) -> None:
    """
    Integration test for send method with Feishu webhook
    Tests actual message sending to Feishu webhook
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    feishu_config = _get_feishu_config()
    assert feishu_config is not None

    # Create test content with various data types
    csv_bytes = b"col1,col2,col3\nvalue1,value2,value3\ndata1,data2,data3"
    test_image_bytes = _create_test_image(150, 150, "green")

    content = NotificationContent(
        name="Superset 测试告警",
        header_data={
            **mock_header_data,
            "notification_type": "Alert",
            "notification_format": "PNG",
            "notification_source": "test",
            "chart_id": 123,
            "dashboard_id": 456,
        },
        description="这是一个集成测试，验证飞书消息发送功能",
        text="测试消息内容：验证飞书 webhook 集成是否正常工作",
        url="https://example.com/dashboard/456",
        csv=csv_bytes,
        screenshots=[test_image_bytes],
    )

    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json=f'{{"target": "{feishu_config["webhook_url"]}"}}',
        ),
        content=content,
    )

    # Mock Flask current_app config
    class MockCurrentApp:
        config = {
            "LARK_APP_ID": feishu_config["app_id"],
            "LARK_APP_SECRET": feishu_config["app_secret"],
            "ALERT_REPORTS_WEBHOOK_HTTPS_ONLY": False,
        }

    monkeypatch.setattr(
        "superset.reports.notifications.webhook.current_app", MockCurrentApp
    )
    monkeypatch.setattr(
        "superset.reports.notifications.webhook.feature_flag_manager.is_feature_enabled",
        lambda flag: True,
    )

    # Send webhook message
    # This should not raise an exception if successful
    webhook_notification.send()

    # If we reach here, the message was sent successfully
    # The actual verification would be checking the Feishu group/chat for the message


@pytest.mark.skipif(
    not _has_feishu_config(),
    reason="Feishu integration tests require LARK_APP_ID, LARK_APP_SECRET, and FEISHU_WEBHOOK_URL environment variables",
)
def test_send_feishu_webhook_without_images_integration(
    mock_header_data, monkeypatch
) -> None:
    """
    Integration test for send method with Feishu webhook without images
    Tests message sending with CSV data but no screenshots
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    feishu_config = _get_feishu_config()
    assert feishu_config is not None

    # Create CSV data
    csv_data = pd.DataFrame(
        {
            "日期": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "销售额": [1000, 2000, 3000],
            "订单数": [10, 20, 30],
        }
    )
    csv_bytes = csv_data.to_csv(index=False).encode("utf-8")

    content = NotificationContent(
        name="数据报表测试",
        header_data=mock_header_data,
        description="测试飞书消息发送（无图片）",
        text="这是一个不包含图片的测试消息",
        url="https://example.com/report/123",
        csv=csv_bytes,
        screenshots=None,
    )

    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json=f'{{"target": "{feishu_config["webhook_url"]}"}}',
        ),
        content=content,
    )

    # Mock Flask current_app config
    class MockCurrentApp:
        config = {
            "LARK_APP_ID": feishu_config["app_id"],
            "LARK_APP_SECRET": feishu_config["app_secret"],
            "ALERT_REPORTS_WEBHOOK_HTTPS_ONLY": False,
        }

    monkeypatch.setattr(
        "superset.reports.notifications.webhook.current_app", MockCurrentApp
    )
    monkeypatch.setattr(
        "superset.reports.notifications.webhook.feature_flag_manager.is_feature_enabled",
        lambda flag: True,
    )

    # Send webhook message
    webhook_notification.send()

    # If we reach here, the message was sent successfully


@pytest.mark.skipif(
    not _has_feishu_config(),
    reason="Feishu integration tests require LARK_APP_ID, LARK_APP_SECRET, and FEISHU_WEBHOOK_URL environment variables",
)
def test_send_feishu_webhook_with_pdf_integration(
    mock_header_data, monkeypatch
) -> None:
    """
    Integration test for send method with Feishu webhook including PDF message
    """
    from superset.reports.models import ReportRecipients, ReportRecipientType
    from superset.reports.notifications.base import NotificationContent

    feishu_config = _get_feishu_config()
    assert feishu_config is not None

    with open("tests/unit_tests/reports/notifications/demo.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    csv_bytes = b"col1,col2\n1,2"

    content = NotificationContent(
        name="PDF 消息测试",
        header_data={
            **mock_header_data,
            "notification_type": "Alert",
            "notification_format": "PDF",
            "notification_source": "test",
        },
        description="这是一个包含 PDF 的集成测试",
        text="测试飞书 PDF 文件消息发送",
        url="https://example.com/report/456",
        csv=csv_bytes,
        pdf=pdf_bytes,
        screenshots=None,
    )

    webhook_notification = WebhookNotification(
        recipient=ReportRecipients(
            type=ReportRecipientType.WEBHOOK,
            recipient_config_json=f'{{"target": "{feishu_config["webhook_url"]}"}}',
        ),
        content=content,
    )

    class MockCurrentApp:
        config = {
            "LARK_APP_ID": feishu_config["app_id"],
            "LARK_APP_SECRET": feishu_config["app_secret"],
            "ALERT_REPORTS_WEBHOOK_HTTPS_ONLY": False,
        }

    monkeypatch.setattr(
        "superset.reports.notifications.webhook.current_app", MockCurrentApp
    )
    monkeypatch.setattr(
        "superset.reports.notifications.webhook.feature_flag_manager.is_feature_enabled",
        lambda flag: True,
    )

    webhook_notification.send()
