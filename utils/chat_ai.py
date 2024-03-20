import os
import json
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),  # "YOUR API KEY",
    base_url="https://api.chatanywhere.tech/v1"
)


def create_empty_json_file():
    if not os.path.exists('env.json'):
        with open('env.json', 'w') as f:
            json.dump({'OPEN_API_USAGE_COUNT': '0'}, f)


def read_open_api_usage_count():
    create_empty_json_file()
    with open('env.json', 'r') as f:
        data = json.load(f)
    cnt = int(data.get('OPEN_API_USAGE_COUNT', '0'))
    print(f"OPENAI_API_USAGE_COUNT : {cnt} times in this hour")
    return cnt


def update_open_api_usage_count(count):
    with open('env.json', 'w') as f:
        json.dump({'OPEN_API_USAGE_COUNT': str(count)}, f)


def get_gpt_35_api_response(messages: list) -> str:
    usage_count = read_open_api_usage_count()
    if usage_count >= 60:
        return "api 已達小時次數限制"

    _messages = [{'role': 'system', 'content': '你是一個有趣幽默但不失智慧的聊天機器人'},]
    for msg in messages:
        _messages.append({'role': 'user', 'content': msg})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=_messages)
    response = completion.choices[0].message.content
    update_open_api_usage_count(usage_count + 1)
    return response

