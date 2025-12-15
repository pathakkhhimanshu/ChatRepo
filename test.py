import requests

API_KEY = "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"

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
     "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "PythonChatbot"
}

data = {
    "model": "nousresearch/nous-hermes-2-mistral-7b:free",
    "messages": [{"role": "user", "content": "Say hello"}],
     "max_tokens": 200
}

r = requests.post(url, headers=headers, json=data)
print(r.status_code)
print(r.text)
