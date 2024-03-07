from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from datetime import datetime

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
import os
import requests


class SCHEDULED_HANDLER:

    HOUR_MSG_DICT = {
        3: "三點了 ！！ 起來重睡 ！！",
        8: "八點了 ！！ 起來早八 ！！",
        12: "十二點了 ！！ 起來進食 ！！",
        15: "下午三點了 ！！ 起來喝下午”茶“ ！！",
    }

    scheduler = BackgroundScheduler()

    line_bot_api: MessagingApi
    configuration: Configuration

    def __init__(self, line_bot_api, configuration):
        self.line_bot_api = line_bot_api
        self.configuration = configuration
        if not self.scheduler.running:
            self.set_schedule()
            self.scheduler.start()

    # def send_hourly_message(self, group_id, name):
    #     hour = datetime.now(timezone('Asia/Taipei')).hour
    #     message_text = self.HOUR_MSG_DICT.get(hour, "測試排程訊息")
    #     message = TextMessage(text=f"{name} {message_text}")
    #     push_message_request = PushMessageRequest(
    #         to=group_id, messages=[message])
    #     self.line_bot_api.push_message(push_message_request)

    def send_hourly_message(self, group_id, name):
        TEST_MODE = False
        hour = datetime.now(timezone('Asia/Taipei')).hour
        message_text = self.HOUR_MSG_DICT.get(hour)
        if not message_text and TEST_MODE:  # 檢查是否在測試模式
            message_text = "測試排程訊息"
        if message_text:  # 只有在 message_text 不為 None 時才發送訊息
            message = TextMessage(text=f"{name} {message_text}")
            push_message_request = PushMessageRequest(
                to=group_id, messages=[message])
            self.line_bot_api.push_message(push_message_request)

    def make_bot_keep_awake(self):
        print("== Make bot keep awake ==")
        requests.get(os.getenv('API_URL', None))

    # Add schedules here

    def set_schedule(self):
        self.scheduler.add_job(self.make_bot_keep_awake, 'interval',
                               minutes=14, timezone=timezone('Asia/Taipei'))
        self.scheduler.add_job(self.send_hourly_message, 'cron', minute=0, second=0, timezone=timezone(
            'Asia/Taipei'), args=["Ca910ecfb8c7289e2c5fc51d58189d01c", "張子儀"])
        # self.scheduler.add_job(self.send_hourly_message, 'cron', second=0, timezone=timezone('Asia/Taipei'), args=["C7f44352f6748f82224d1c211175ae839", "張子儀"])

    def handle(self):
        pass
