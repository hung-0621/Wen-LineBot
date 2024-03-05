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

# from linebot.models import ImageSendMessage
import requests
from typing import Callable, Dict
import random


class CMD_HANDLER:

    event: MessageEvent
    line_bot_api: MessagingApi

    RANDOM_SENTENCE_URL = "https://api.vvhan.com/api/ian"

    def get_response_from_url(self) -> str:
        response = requests.get(self.RANDOM_SENTENCE_URL)
        return response.text

    def send_image(self, url):
        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[ImageMessage(
                    originalContentUrl=url, previewImageUrl=url)]
            )
        )

    def send_message(self, msg):
        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[TextMessage(
                    text=msg)]
            )
        )

    def send_image_with_msg(self, url, msg):
        image_message = ImageMessage(
            originalContentUrl=url, previewImageUrl=url)
        text_message = TextMessage(text=msg)

        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[image_message, text_message]
            )
        )

    cmd_dict: Dict[str, Callable[[], None]] = {}

    def key_is_in_dict(self, key) -> bool:
        return key in self.cmd_dict

    def get_dict_value(self, key) -> any:
        value = self.cmd_dict[key]
        if callable(value):
            return value  # Don't execute the function here
        return value


    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        self.cmd_dict["嗨張子儀"] = lambda: self.send_message(
            "嗨張子儀，今天的張子儀也很張子儀，今天義大利麵也要記得拌42號混凝土ㄛ")
        self.cmd_dict["欸張子儀"] = lambda: self.send_message(
            "欸張子儀，"+self.get_response_from_url())
        # self.cmd_dict["我覺得你說的對"] = lambda: self.send_message("我覺得你說的對，但是我要補充一下，首先袋鼠的祖先是一條長頸鹿，而火星表面並沒有任何關於鴨嘴獸生活的痕跡，所以我並不認可湖南人不能吃辣的問題。其次亞特蘭蒂斯是在公元前十年，在賽博坦星球被來自m78星雲來的假面騎士給毀滅的，所以才有了後面著名的通古斯大爆炸，但是答案是紫色的，因為外星人不戴帽子，今天下雨生吃冰箱會降火，而且把手機丟到麻辣燙裡的話會更入味，另外依古比古的毛毯好像是紅色的，這事也不能全怪拜登，畢竟數學不好也不是一個人的事，需要夫妻雙方一起努力那樣就算不成功，房頂也最少能放三張大餅，再多就很辣了！總的來說，我個人還是比較喜歡意大利菜的，當然也不介意去遊個泳，這個季節最適合睡覺，因為我在美國的飛機上，而你卻在火星上面打袋鼠！可是這篇文章所描述的，並不是外星人能否扎辮子。所以你所說的論語其實是對的，但是我只想說：烏拉圭的石油在醫院裡面真的很吃香。我作為一個地地道道的非洲白人對於理智的瘋子來說，我的秘密是不能告訴新西蘭的猩猩的，所以你會覺得我很菜嗎 ？你絕對會，因為昨天的豬頭剃了個光頭。但其實真正遵致這個問題的起源是GTA5 很貴，我認為這個價錢可能跟你的哥哥沒有關係，因為老鼠把我的鼻屎吃了，你能理解嗎 ？我最開始為什麼不認可你。但是有一說一酸奶烘焙健康早餐不好吃，因為微積分的小數點變成了句號，而我旁邊的猴子是金猴因此它的手裡拿了嗩吶。你的觀點大體上是沒錯的，但是你沒考慮到剛果的總統是黑人。總而言之這個和你的作息有關，你可以試一試把新鮮的帶魚放在頭上。我的手機要沒電了，這並不影響加拿大的冰。我喝的是美味的燕湖江水，因此美國的總統是薩科而且蒙古的海軍十分強大，我認為我的邏輯沒有問題因為羅技是個大牌子。嚴肅來說根據刑法第 114514條的規定，我的窗簾已經拉開了。總而言之：愛迪生真的不會說英語。你還違背了獵豹的拇指定律因為為猩猩的體毛是電腦形狀的，但是你不在乎，因為你只在乎義大利麵要拌 42 號混凝士。對吧？")
        self.cmd_dict["我個人認為"] = lambda: self.send_message(
            "我個人認為義大利麵就應該拌42號混凝土，因為這個螺絲釘的長度很容易直接影響到挖掘機的扭矩。你往裡砸的時候，一瞬間他就會產生大量的高蛋白，俗稱UFO，會嚴重影響經濟的發展，以至於對整個太平洋，和充電器的核污染。再者說透過勾股定理很容易推斷出人工飼養的東條英機，他是可以捕獲野生的三角函數，所以說不管這秦始皇的切面是否具有放射性，特朗普的N次方是否含有沈澱物，都不影響到沃爾瑪跟維爾康在南極會合。")
        self.cmd_dict["菜就多練"] = lambda: self.send_message(
            "菜就多練，輸不起就別玩，以前是以前，現在是現在，哥們你老是拿以前比那你怎麼不拿你剛出生比")
        self.cmd_dict["你說的對"] = lambda: self.send_message(
            "你說的對，但是烏拉圭的人口有345.7萬，同時，僅澳大利亞就有4700萬隻袋鼠。如果袋鼠決定入侵烏拉圭，那麼每一個烏拉圭人都要打14隻袋鼠，你不知道，你不在乎，你只關心你自己。")
        self.cmd_dict["沒錯只有你"] = lambda: self.send_message(
            "沒錯只有你，你是智慧的結晶，你是文明的瑰寶，你是人類的獨苗，你是上帝的遺珠，你是雨後的彩虹，你是夤夜的皎月，你是晨昏的彩霞，你是銀河的唯一，你是樹枝的芽杈，你是滄海的珊瑚，你是最後的希望，你是問題的正解，你是莫蒂的瑞克，你是法國的拿破崙，你是歷史的書寫者，你是人類的光明，你是電你是光你是唯一的神話")
        self.cmd_dict["padoru"] = lambda: self.send_message(
            "hasi re so ri yo\nkaze no you ni\ntsuki mi hara wo\nPADORU！PADORU！")
        self.cmd_dict["張子儀不會"] = lambda: self.send_message(
            "張子儀不會，可是"+random.choice(["李多慧", "茶湯會", "獅子會", "紅十字會", "光明會"]))
        self.cmd_dict["喝水水"] = lambda: self.send_image_with_msg(url="https://raw.githubusercontent.com/Wen-Line-Bot/Wen-LineBot/main/images/drink_water.jpg",msg="水量++")

        help_msg = """
這是本機器人操作指令說明
--------------------
可用指令：\n
""" + "\n".join([f"- {k}" for k in self.cmd_dict.keys()])

        self.cmd_dict["bot help"] = lambda: self.send_message(help_msg)

    def handle(self):
        pass


# https://github.com/Wen-Line-Bot/Wen-LineBot/blob/main/images/drink_water.png?raw=true
