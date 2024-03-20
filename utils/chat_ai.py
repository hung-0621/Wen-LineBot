import os
import json

import google.generativeai as genai

def get_ai_response(message: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key=os.getenv('GIMINI_API_KEY', None))
    response = model.generate_content(f"<請扮演一個有趣幽默不失智慧的人，像普通人一樣回覆訊息>{message}",safety_settings={'HARASSMENT':'block_none'})
    return response.text

