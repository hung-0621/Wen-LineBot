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

# from linebot.models import ImageSendMessage
import requests
from typing import Callable, Dict
import random


class EVENT_HANDLER:

    event: MessageEvent
    line_bot_api: MessagingApi

    cmd_dict: Dict[str, Callable[[], None]] = {}

    def key_is_in_dict(self, key) -> bool:
        return key in self.cmd_dict

    def get_dict_value(self, key) -> any:
        value = self.cmd_dict[key]
        if callable(value):
            return value  # Don't execute the function here
        return value


    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        

    def handle(self):
        pass


