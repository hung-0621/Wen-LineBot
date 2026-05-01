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
import utils.my_func as my_func
from flask import current_app as app


class LineHelper:
    def __init__(self, line_bot_api: MessagingApi, event: MessageEvent):
        self.line_bot_api = line_bot_api
        self.event = event

    def send_image(self, url: str):
        try:
            self.line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=self.event.reply_token,
                    messages=[ImageMessage(
                        originalContentUrl=url, previewImageUrl=url)]
                )
            )
        except Exception as e:
            app.logger.error(f"Error in send_image: {e}")

    def send_message(self, msg: str):
        try:
            self.line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=self.event.reply_token,
                    messages=[TextMessage(text=msg)]
                )
            )
        except Exception as e:
            app.logger.error(f"Error in send_message: {e}")

    def send_image_with_msg(self, url: str, msg: str):
        try:
            image_message = ImageMessage(
                originalContentUrl=url, previewImageUrl=url)
            text_message = TextMessage(text=msg)

            self.line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=self.event.reply_token,
                    messages=[image_message, text_message]
                )
            )
        except Exception as e:
            app.logger.error(f"Error in send_image_with_msg: {e}")

    def send_complex_message(self, message_list: list):
        try:
            self.line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=self.event.reply_token,
                    messages=message_list
                )
            )
        except Exception as e:
            app.logger.error(f"Error in send_complex_message: {e}")