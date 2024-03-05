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

class SCHEDULED_HANDLER:

    HOUR_MSG_DICT = {
        3: "三點了 ！！ 起來重睡 ！！",
        8: "八點了 ！！ 起來早八 ！！",
        12: "十二點了 ！！ 起來進食 ！！",
        15: "下午三點了 ！！ 起來喝下午”茶“ ！！",
    }

    scheduler = BackgroundScheduler()

    event: MessageEvent
    line_bot_api: MessagingApi
    configuration: Configuration

    def __init__(self,event,line_bot_api,configuration):
        self.event = event
        self.line_bot_api = line_bot_api
        self.configuration = configuration
        self.set_schedule()
        self.scheduler.start()


    def send_hourly_message(self,group_id, name):
        hour = datetime.now(timezone('Asia/Taipei')).hour
        message_text = self.HOUR_MSG_DICT.get(hour,"測試排程訊息")
        message = TextMessage(text=f"{name} {message_text}")
        push_message_request = PushMessageRequest(to=group_id, messages=[message])
        self.line_bot_api.push_message(push_message_request)


    def set_schedule(self):
        self.scheduler.add_job(self.send_hourly_message, 'cron', minute=0, second=0, timezone=timezone('Asia/Taipei'), args=["Ca910ecfb8c7289e2c5fc51d58189d01c", "張子儀"])
        self.scheduler.add_job(self.send_hourly_message, 'cron', second=0, timezone=timezone('Asia/Taipei'), args=["C7f44352f6748f82224d1c211175ae839", "張子儀"])

    def handle(self):
        pass
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(self.send_hourly_message, 'cron', minute=0, second=0, timezone=timezone('Asia/Taipei'), args=["Ca910ecfb8c7289e2c5fc51d58189d01c", "張子儀"])
        # #scheduler.add_job(self.send_hourly_message, 'cron', second=0, timezone=timezone('Asia/Taipei'), args=["C7f44352f6748f82224d1c211175ae839", "張子儀"])
        # scheduler.start()
