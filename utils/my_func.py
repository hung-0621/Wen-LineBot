import random
import requests
from pypinyin import lazy_pinyin, pinyin, Style
import re
import json
import utils.vars_consts as vars_consts
from bs4 import BeautifulSoup


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


def get_image_url_by_search(search_query: str) -> str:
    try:
        # Define the URL of the search engine (e.g., Google Images)
        search_url = f"https://www.google.com/search?q={search_query}&tbm=isch"

        # Send an HTTP request to the search URL
        response = requests.get(search_url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all image tags
        img_tags = soup.find_all("img")

        # Extract image URLs
        image_urls = [img["src"] for img in img_tags if "src" in img.attrs]

        # Filter out non-image URLs (e.g., icons)
        image_urls = [url for url in image_urls if url.startswith("http")]

        # Choose a random image URL
        random_image_url = random.choice(image_urls)
        print(random_image_url)
        return random_image_url
    except Exception as e:
        return str(e)
