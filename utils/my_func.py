import random
import requests
from pypinyin import lazy_pinyin, pinyin, Style
import re
import json
import utils.vars_consts as vars_consts
from bing_image_urls import bing_image_urls


def get_response_text_from_url(url) -> str:
    response = requests.get(url=url)
    return response.text


def contains_pinyin(target_pinyin, text):
    # 將句子轉換為拼音
    text_pinyin = ' '.join([i[0] for i in pinyin(text, style=Style.TONE)])
    print(text_pinyin)
    # 使用正則表達式匹配目標詞的拼音
    return bool(re.search(target_pinyin, text_pinyin))


def get_one_rand_cat_image_url() -> str:
    parsed_data = json.loads(
        get_response_text_from_url(vars_consts.RANDOM_CAT_URL))
    return parsed_data[0]['url']


def get_image_url_by_search(search_query: list[str]) -> str:
    urls_list = []
    try:
        for sq in search_query:
            urls = bing_image_urls(sq, limit=20)
            urls_list.extend(urls)
        urls_set = set(urls_list)
        url = random.choice(urls_set)
        print(f"{url} , selected in {len(urls_set)} urls")
        return url
    except Exception as e:
        return str(e)
