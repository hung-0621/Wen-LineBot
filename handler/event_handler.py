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

import requests
from typing import Callable, Dict
from LineHelper import LineHelper
import random
import utils.my_func as my_func


class EVENT_HANDLER:

    event: MessageEvent
    line_bot_api: MessagingApi
    line_helper: LineHelper
    event_list: list

    def __init__(self, event, line_bot_api, line_helper):
        self.event = event
        self.line_bot_api = line_bot_api
        self.line_helper = line_helper
        self.event_list = [self.wo_can_yuan,self.feng_bin]

    def wo_can_yuan(self):
        if my_func.contains_pinyin("yuán", self.event.message.text):
            self.line_helper.send_message("沃草 原！")

    def feng_bin(self):
        if my_func.contains_pinyin("fēng bīn", self.event.message.text):
            self.line_helper.send_image(
                f"https://raw.githubusercontent.com/Wen-Line-Bot/Wen-LineBot/main/images/feng_bin/feng_bin_{random.randint(0,9)}.jpg")

    def handle(self):
        for event in self.event_list:
            event()
