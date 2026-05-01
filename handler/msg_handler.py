from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    PushMessageRequest,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from flask import current_app as app

from enums.response_type import ResponseType
from handler.cmd_handler import CMD_HANDLER
from handler.event_handler import EVENT_HANDLER
from LineHelper import LineHelper


class MSG_HANDLER:

    event: MessageEvent
    line_bot_api: MessagingApi
    configuration: Configuration

    cmd_handler: CMD_HANDLER
    event_handler: EVENT_HANDLER

    line_helper: LineHelper

    def __init__(
        self,
        event,
        line_bot_api,
        configuration,
        cmd_handler,
        event_handler,
        line_helper,
    ):
        self.event = event
        self.line_bot_api = line_bot_api
        self.configuration = configuration
        self.cmd_handler = cmd_handler
        self.event_handler = event_handler
        self.line_helper = line_helper

    def cmd_handle(self):
        try:
            key = self.event.message.text
            if key.replace(" ", "").lower() == "bothelp":
                key = "bot help"

            if self.cmd_handler.key_is_in_dict(
                key
            ):  # and self.event.source.type == "group"):
                response_message: tuple = self.cmd_handler.get_dict_value(key)
            else:
                return

            self.send_message(response_message)
        except Exception as e:
            app.logger.error(f"Error in cmd_handle: {e}")

    # 調用 line_helper 回傳訊息
    # messgae -> (type, message) or (type, image_url) or (type, image_url, message)
    def send_message(self, message: tuple):
        try:
            if message[0] == ResponseType.TEXT:
                self.line_helper.send_message(message[1])
            elif message[0] == ResponseType.IMAGE:
                self.line_helper.send_image(message[1])
            elif message[0] == ResponseType.IMAGE_MSG:
                self.line_helper.send_image_with_msg(message[1], message[2])
        except Exception as e:
            app.logger.error(f"Error in send_message: {e}")

    def event_handle(self):
        try:
            self.event_handler.handle()
        except Exception as e:
            app.logger.error(f"Error in event_handle: {e}")

    def dump_handled_message(self):
        try:
            source_type = self.event.source.type
            if source_type == "group":
                group_id = self.event.source.group_id
                user_id = self.event.source.user_id
                app.logger.info(f"Group ID: {group_id} ; User ID: {user_id}")
            elif source_type == "user":
                user_id = self.event.source.user_id
                app.logger.info(f"User ID: {user_id}")

            # Get the user's message
            user_message = self.event.message.text
            app.logger.info(f"User Message: {user_message}")
        except Exception as e:
            app.logger.error(f"Error in dump_handled_message: {e}")

    def handle(self):
        try:
            func_handlers: list[function] = [
                self.dump_handled_message,
                self.cmd_handle,
                self.event_handle,
            ]
            for func in func_handlers:
                func()
        except Exception as e:
            app.logger.error(f"Error in MSG_HANDLER handle: {e}")
