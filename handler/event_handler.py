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
        self.event_list = [self.wo_can_yuan, self.feng_bin, self.hao_hu]

    def wo_can_yuan(self) -> TextMessage:
        if my_func.contains_pinyin("yuán", self.event.message.text):
            return TextMessage(text="沃草 原！")

    def feng_bin(self) -> ImageMessage:
        if my_func.contains_pinyin("fēng bīn", self.event.message.text):
            url = f"https://raw.githubusercontent.com/Wen-Line-Bot/Wen-LineBot/main/images/feng_bin/feng_bin_{random.randint(0,9)}.jpg"
            return ImageMessage(
                originalContentUrl=url, previewImageUrl=url)

    def hao_hu(self) -> list:
        if my_func.contains_pinyin("hǎo hú", self.event.message.text):
            url_list_1 = my_func.get_image_url_list_by_search(
                "Fubuki Shirakami")
            url_list_2 = my_func.get_image_url_list_by_search("白上吹雪")
            url_list_3 = my_func.get_image_url_list_by_search("白上 フブキ")
            url_list = url_list_1+url_list_2+url_list_3
            url = random.choice(url_list)
            print(f"好狐 url : {url}")
            return [ImageMessage(
                originalContentUrl=url, previewImageUrl=url), TextMessage(text="好狐")]

    def handle(self):
        message_list = []
        for event in self.event_list:
            e = event()
            if e != None:
                if isinstance(e, list):
                    message_list.extend(e)
                else:
                    message_list.append(e)
        if message_list != []:
            self.line_helper.send_complex_message(message_list)
