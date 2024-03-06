import requests
from pypinyin import lazy_pinyin
import re

def get_response_text_from_url(url) -> str:
    response = requests.get(url=url)
    return response.text

def contains_yuan_pronunciation(text):
    target_pinyin = "yuan"
    # 將句子轉換為拼音
    text_pinyin = ' '.join(lazy_pinyin(text))
    print(text_pinyin)
    # 使用正則表達式匹配目標詞的拼音
    return bool(re.search(target_pinyin, text_pinyin))