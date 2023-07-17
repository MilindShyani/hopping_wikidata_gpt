import json
import requests

def gpt_call(api_key):
    api_key = api_key
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Translate the following English text to Spanish: '{I am a boy}'"}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response.json())