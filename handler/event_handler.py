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
import asyncio
from typing import Callable, Dict
from LineHelper import LineHelper
import random
import utils.my_func as my_func
import utils.chat_ai as chat_ai


class EVENT_HANDLER:

    event: MessageEvent
    line_bot_api: MessagingApi
    line_helper: LineHelper
    event_list: list

    def __init__(self, event, line_bot_api, line_helper):
        self.event = event
        self.line_bot_api = line_bot_api
        self.line_helper = line_helper
        self.event_list = [self.chat_with_ai, self.wo_can_yuan,
                           self.feng_bin, self.hao_hu]

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
            url = my_func.get_image_url_by_search(
                search_query=["白上吹雪", "白上 フブキ", "Fubuki Shirakami"])
            return [ImageMessage(
                originalContentUrl=url, previewImageUrl=url), TextMessage(text="好狐")]

    async def chat_with_ai(self) -> TextMessage:
        pattern = "誒機器人"
        msg = self.event.message.text
        if msg.startswith(pattern):
            msg = msg.replace(pattern, '', 1)
            response = chat_ai.get_gpt_35_api_response(messages=[msg])
            cnt = chat_ai.read_open_api_usage_count()
            response += f"\n\n<< API_USAGE_COUNT >>\n{cnt} times in this hour"
            return TextMessage(text=response)

    def handle(self):
        message_list = []
        for event in self.event_list:
            e = asyncio.run(event()) if asyncio.iscoroutinefunction(
                event) else event()
            if e != None:
                if isinstance(e, list):
                    message_list.extend(e)
                else:
                    message_list.append(e)
        if message_list != []:
            self.line_helper.send_complex_message(message_list)
