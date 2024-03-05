from datetime import datetime
import os
from flask import Flask, request, abort
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

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

from handler.msg_handler import MSG_HANDLER
from handler.cmd_handler import CMD_HANDLER

app = Flask(__name__)

configuration = Configuration(
    access_token=os.getenv('CHANNEL_ACCESS_TOKEN', None))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', None))


messages = {
    3: "三點了 ！！ 起來重睡 ！！",
    8: "八點了 ！！ 起來早八 ！！",
    12: "十二點了 ！！ 起來進食 ！！",
    15: "下午三點了 ！！ 起來喝下午”茶“ ！！",
}

def send_hourly_message(group_id, name):
    hour = datetime.now(timezone('Asia/Taipei')).hour
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        message_text = messages.get(hour,"測試排程訊息")
        message = TextMessage(text=f"{name} {message_text}")
        push_message_request = PushMessageRequest(to=group_id, messages=[message])
        line_bot_api.push_message(push_message_request)

scheduler = BackgroundScheduler()
scheduler.add_job(send_hourly_message, 'cron', minute=0, second=0, timezone=timezone('Asia/Taipei'), args=["Ca910ecfb8c7289e2c5fc51d58189d01c", "張子儀"])
# scheduler.add_job(send_hourly_message, 'cron', second=0, timezone=timezone('Asia/Taipei'), args=["C7f44352f6748f82224d1c211175ae839", "張子儀"])
scheduler.start()




@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
    cmd_handler = CMD_HANDLER()
    msg_handler = MSG_HANDLER(event=event,configuration=configuration,line_bot_api=line_bot_api,cmd_handler=cmd_handler)
    msg_handler.handle()


if __name__ == "__main__":
    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
