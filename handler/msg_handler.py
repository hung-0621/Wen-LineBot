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
    PushMessageRequest
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from handler.cmd_handler import CMD_HANDLER

class MSG_HANDLER:

    event: MessageEvent
    line_bot_api: MessagingApi
    configuration: Configuration
    
    cmd_handler:CMD_HANDLER

    def __init__(self, event, line_bot_api,configuration,cmd_handler):
        self.event = event
        self.line_bot_api = line_bot_api
        self.configuration = configuration
        self.cmd_handler = cmd_handler

    def cmd_handle(self):
        key = self.event.message.text
        if key.replace(" ", "").lower() == "bothelp":
            key = "bot help"
        if (self.cmd_handler.key_is_in_dict(key) and self.event.source.type == "group"):
            self.cmd_handler.get_dict_value(key)()
        #     self.line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=self.event.reply_token,
        #         messages=[TextMessage(text=self.cmd_handler.get_dict_value(key=key))]
        #     )
        # )

    def dump_handled_message(self):
        source_type = self.event.source.type
        if source_type == "group":
            group_id = self.event.source.group_id
            user_id = self.event.source.user_id
            print(f"Group ID: {group_id} ; User ID: {user_id}")
        elif source_type == "user":
            user_id = self.event.source.user_id
            print(f"User ID: {user_id}")

        # Get the user's message
        user_message = self.event.message.text
        print(user_message)

        print()

    def handle(self):
        func_handlers:list[function] = [self.dump_handled_message, self.cmd_handle]
        for func in func_handlers:
            func()