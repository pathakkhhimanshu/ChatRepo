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
    "model": "mistralai/mistral-7b-instruct:free",
    "messages": [{"role": "user", "content": "Say hello"}]
}

r = requests.post(url, headers=headers, json=data)
print(r.status_code)
print(r.text)
