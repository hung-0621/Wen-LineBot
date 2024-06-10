import os
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


def get_response_text_from_url_params(url, params) -> str:
    response = requests.get(url=url, params=params)
    return response.text


def contains_pinyin(target_pinyin, text):
    # 將句子轉換為拼音
    text_pinyin = ' '.join([i[0] for i in pinyin(text, style=Style.TONE)])
    # print(text_pinyin)
    # 使用正則表達式匹配目標詞的拼音
    return bool(re.search(target_pinyin, text_pinyin))


def get_one_rand_cat_image_url() -> str:
    parsed_data = json.loads(
        get_response_text_from_url(vars_consts.RANDOM_CAT_URL))
    return parsed_data[0]['url']


def get_one_rand_waifu_image_url() -> str:
    parsed_data = json.loads(
        get_response_text_from_url(vars_consts.RANDOM_WAIFU_URL))
    return parsed_data["images"][0]["url"]


def get_image_url_by_search(search_query: list[str]) -> str:
    urls_list = []
    try:
        for sq in search_query:
            urls = bing_image_urls(sq, limit=20)
            urls_list.extend(urls)
        urls_set = set(urls_list)
        url = random.choice(list(urls_set))
        print(f"{url} , selected in {len(urls_set)} urls")
        return url
    except Exception as e:
        return str(e)

# blue archive funcs ...
def fetch_bluearchive_chars():
    parsed_data = json.loads(
        get_response_text_from_url(vars_consts.RANDOM_BLUE_ARCHIVE_CHARS_URL))
    write_to_json(vars_consts.BA_CHARS_JSON_PATH,parsed_data)

# filename example : foo.json
def write_to_json(filename: str, content: str):
    if not os.path.exists(vars_consts.JSON_DIRECTORY):
        os.mkdir(vars_consts.JSON_DIRECTORY)
    with open(os.path.join(vars_consts.JSON_DIRECTORY, filename), 'w') as f:
        json.dump(content, f)
        f.close()

def delete_file(filepath:str):
    if os.path.exists(filepath):
        os.remove(filepath)

def init_bluearchive_chars_data():
    delete_file(vars_consts.BA_CHARS_JSON_PATH)
    fetch_bluearchive_chars()

def get_one_rand_bluearchive_char_id() -> int:
    with open(vars_consts.BA_CHARS_JSON_PATH, 'r') as f:
        data = json.load(f)
        # print(random.choice(data))
        f.close()
        return random.choice(data)["id"]

def get_bluearchive_char_detail_data(id:int) -> list:
    parsed_data = json.loads(
        get_response_text_from_url(f"{vars_consts.BLUE_ARCHIVE_BASE_API_URL}/character/{id}?id=true"))
    print(parsed_data)
    name = parsed_data["character"]["name"].split()[0]
    age = parsed_data["info"]["age"]
    portrait = parsed_data["image"]["portrait"]
    extra_msg : str = ""
    try:
        age_value = int(age.split()[0])
    except :
        extra_msg = "啊？"
    else:
        if age_value >= 18:
            extra_msg = "謝嘍。好沒感覺"
        else:
            extra_msg = "謝謝！好有感覺！！"

    return [name,age,portrait,extra_msg]