from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    PushMessageRequest,
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)


class LineHelper:
    def __init__(self, line_bot_api: MessagingApi, event: MessageEvent):
        self.line_bot_api = line_bot_api
        self.event = event

    def send_image(self, url: str):
        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[ImageMessage(
                    originalContentUrl=url, previewImageUrl=url)]
            )
        )

    def send_message(self, msg: str):
        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

    def send_image_with_msg(self, url: str, msg: str):
        image_message = ImageMessage(
            originalContentUrl=url, previewImageUrl=url)
        text_message = TextMessage(text=msg)

        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[image_message, text_message]
            )
        )
