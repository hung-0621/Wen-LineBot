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
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)

configuration = Configuration(
    access_token=os.getenv('CHANNEL_ACCESS_TOKEN', None))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', None))


def send_daily_message():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # Replace 'YOUR_GROUP_ID' with the actual ID of your group
        # Replace 'USER_ID' with the actual ID of the user you want to mention
        line_bot_api.push_message('YOUR_GROUP_ID', TextMessage(text="<@USER_ID> 三點了 ！！ 起來重睡 ！！"))


scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_message, 'cron', hour=3, minute=0, second=0, timezone=timezone('Asia/Taipei'))
# scheduler.start()


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


def greetToYee(event: MessageEvent, line_bot_api: MessagingApi):
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text="嗨張子儀，今天的張子儀也很張子儀，今天義大利麵也要記得拌42號混凝土ㄛ")]
        )
    )


def defaultMsg(event: MessageEvent, line_bot_api: MessagingApi):
    line_bot_api.reply_message_with_http_info(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)]
        )
    )


def dump_handled_message(event):
    source_type = event.source.type
    if source_type == "group":
        group_id = event.source.group_id
        print(f"Group ID: {group_id}")
    elif source_type == "user":
        user_id = event.source.user_id
        print(f"User ID: {user_id}")

    # Get the user's message
    user_message = event.message.text
    # print(f"User's message: {user_message}")

    # Get the user's profile information
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        profile = line_bot_api.get_profile(user_id)
        print(f"User's name: {profile.display_name}\nmessage: {user_message}")

    print()


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        dump_handled_message(event=event)
        if event.message.text == "嗨張子儀" and event.source.type == "group":
            print(f"Group ID: {event.source.group_id}")
            greetToYee(event=event, line_bot_api=line_bot_api)
        else:
            pass
            # defaultMsg(event=event, line_bot_api=line_bot_api)


if __name__ == "__main__":
    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
