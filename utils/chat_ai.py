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
        f"<請扮演一個有趣幽默不失智慧的人，像普通人一樣回覆訊息，並快速給我簡短的回應>{message}", safety_settings=safety_settings)
    return response.text
