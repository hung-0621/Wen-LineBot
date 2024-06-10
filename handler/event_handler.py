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
        self.event_list = [self.wo_can_yuan,
                           self.wo_chao_ming,
                           self.dang_an,
                           self.feng_bin,
                           self.hao_ke_lian_o,
                           self.hao_hu,
                           self.chat_with_ai]

    def wo_can_yuan(self) -> TextMessage:
        if my_func.contains_pinyin("yuán", self.event.message.text):
            return TextMessage(text="沃草 原！")

    def wo_chao_ming(self) -> TextMessage:
        if my_func.contains_pinyin("míng", self.event.message.text):
            return TextMessage(text="沃潮 鳴！")

    def dang_an(self) -> list:
        if my_func.contains_pinyin("dàng àn", self.event.message.text):
            id = my_func.get_one_rand_bluearchive_char_id()
            data = my_func.get_bluearchive_char_detail_data(id)
            url = data[2]
            text_msg_1 = f"name : {data[0]}\nage : {data[1]}\n{data[3]}"
            return [TextMessage(text="什麼檔案？藍色的嗎？"),ImageMessage(
                originalContentUrl=url, previewImageUrl=url),TextMessage(text=text_msg_1)]

    def feng_bin(self) -> ImageMessage:
        if my_func.contains_pinyin("fēng bīn", self.event.message.text):
            url = f"https://raw.githubusercontent.com/Wen-Line-Bot/Wen-LineBot/main/images/feng_bin/feng_bin_{random.randint(0, 9)}.jpg"
            return ImageMessage(
                originalContentUrl=url, previewImageUrl=url)

    def hao_ke_lian_o(self) -> TextMessage:
        if my_func.contains_pinyin("hǎo kě lián ō", self.event.message.text):
            return TextMessage(text="好可憐喔，陳威嗚嗚嗚嗚嗚😭")

    def hao_hu(self) -> list:
        if my_func.contains_pinyin("hǎo hú", self.event.message.text):
            url = my_func.get_image_url_by_search(
                search_query=["白上吹雪", "白上 フブキ", "Fubuki Shirakami"])
            return [ImageMessage(
                originalContentUrl=url, previewImageUrl=url), TextMessage(text="好狐")]

    def chat_with_ai(self) -> TextMessage:
        pattern = "誒機器人"
        pattern2 = "欸機器人"
        msg = self.event.message.text
        response = None
        if msg.startswith(pattern) or msg.startswith(pattern2):
            msg = msg[4:]
            print(f"CHAT WITH AI : {msg}")
            print("Getting gemini response ...")
            response = chat_ai.get_ai_response(message=msg)
            print("Response from AI:", response)  # Debugging statement
            if response:
                return TextMessage(text=response)
            else:
                return TextMessage(text="Sorry, I couldn't generate a response at the moment.")

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
