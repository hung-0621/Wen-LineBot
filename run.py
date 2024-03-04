import os
from flask import Flask, request, abort

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


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        if event.message.text == "嗨張子儀" and event.source.type == "group":
            greetToYee(event=event, line_bot_api=line_bot_api)
        else:
            pass
            # defaultMsg(event=event, line_bot_api=line_bot_api)


if __name__ == "__main__":
    app.run()
