import os

RANDOM_SENTENCE_URL = "https://api.vvhan.com/api/ian/rand"
RANDOM_CAT_URL = "https://api.thecatapi.com/v1/images/search"
RANDOM_WAIFU_URL = "https://api.waifu.im/search"
RANDOM_BLUE_ARCHIVE_CHARS_URL = "https://api.ennead.cc/buruaka/character"
BLUE_ARCHIVE_BASE_API_URL = "https://api.ennead.cc/buruaka"

CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
JSON_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "json")


# json file paths for tmp storage
BA_CHARS_JSON_PATH =  os.path.join(JSON_DIRECTORY, "blue_archive_chars.json")