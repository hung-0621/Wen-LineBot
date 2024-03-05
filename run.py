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
#scheduler.add_job(send_hourly_message, 'cron', minute=0, second=0, timezone=timezone('Asia/Taipei'), args=["Ca910ecfb8c7289e2c5fc51d58189d01c", "張子儀"])
scheduler.add_job(send_hourly_message, 'cron', second=0, timezone=timezone('Asia/Taipei'), args=["Ca910ecfb8c7289e2c5fc51d58189d01c", "張子儀"])
scheduler.start()



CMD_DICT = {
    "嗨張子儀":"嗨張子儀，今天的張子儀也很張子儀，今天義大利麵也要記得拌42號混凝土ㄛ",
    "我覺得你說的對":"我覺得你說的對，但是我要補充一下，首先袋鼠的祖先是一條長頸鹿，而火星表面並沒有任何關於鴨嘴獸生活的痕跡，所以我並不認可湖南人不能吃辣的問題。其次亞特蘭蒂斯是在公元前十年，在賽博坦星球被來自m78星雲來的假面騎士給毀滅的，所以才有了後面著名的通古斯大爆炸，但是答案是紫色的，因為外星人不戴帽子，今天下雨生吃冰箱會降火，而且把手機丟到麻辣燙裡的話會更入味，另外依古比古的毛毯好像是紅色的，這事也不能全怪拜登，畢竟數學不好也不是一個人的事，需要夫妻雙方一起努力那樣就算不成功，房頂也最少能放三張大餅，再多就很辣了！總的來說，我個人還是比較喜歡意大利菜的，當然也不介意去遊個泳，這個季節最適合睡覺，因為我在美國的飛機上，而你卻在火星上面打袋鼠！可是這篇文章所描述的，並不是外星人能否扎辮子。所以你所說的論語其實是對的，但是我只想說：烏拉圭的石油在醫院裡面真的很吃香。我作為一個地地道道的非洲白人對於理智的瘋子來說，我的秘密是不能告訴新西蘭的猩猩的，所以你會覺得我很菜嗎 ？你絕對會，因為昨天的豬頭剃了個光頭。但其實真正遵致這個問題的起源是GTA5 很貴，我認為這個價錢可能跟你的哥哥沒有關係，因為老鼠把我的鼻屎吃了，你能理解嗎 ？我最開始為什麼不認可你。但是有一說一酸奶烘焙健康早餐不好吃，因為微積分的小數點變成了句號，而我旁邊的猴子是金猴因此它的手裡拿了嗩吶。你的觀點大體上是沒錯的，但是你沒考慮到剛果的總統是黑人。總而言之這個和你的作息有關，你可以試一試把新鮮的帶魚放在頭上。我的手機要沒電了，這並不影響加拿大的冰。我喝的是美味的燕湖江水，因此美國的總統是薩科而且蒙古的海軍十分強大，我認為我的邏輯沒有問題因為羅技是個大牌子。嚴肅來說根據刑法第 114514條的規定，我的窗簾已經拉開了。總而言之：愛迪生真的不會說英語。你還違背了獵豹的拇指定律因為為猩猩的體毛是電腦形狀的，但是你不在乎，因為你只在乎義大利麵要拌 42 號混凝士。對吧？"
}


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
            messages=[TextMessage(text=CMD_DICT[event.message.text])]
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
        # print(f"Group ID: {group_id}")
        user_id = event.source.user_id
        print(f"Group ID: {group_id} ; User ID: {user_id}")
    elif source_type == "user":
        user_id = event.source.user_id
        print(f"User ID: {user_id}")

    # Get the user's message
    user_message = event.message.text

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
        # dump_handled_message(event=event)
        if event.message.text in CMD_DICT and event.source.type == "group":
            # print(f"Group ID: {event.source.group_id}")
            greetToYee(event=event, line_bot_api=line_bot_api)
        else:
            pass
            # defaultMsg(event=event, line_bot_api=line_bot_api)


if __name__ == "__main__":
    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
