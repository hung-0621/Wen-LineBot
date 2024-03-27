import os
import json

import google.generativeai as genai

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]


def get_ai_response(message: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key=os.getenv('GIMINI_API_KEY', None))
    response = model.generate_content(
        f"<你是有趣幽默又聰明的人，使用繁體中文像普通人一樣進行對話>。{message}", safety_settings=safety_settings)
    return response.text
