import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("OPENROUTER_API_KEY not found. Add it to .env")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
     "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "MyChatbot"
}

def ask_openrouter(message, model="meta-llama/llama-3.1-8b-instruct:free"):
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }
    resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    
    return data["choices"][0]["message"]["content"]

def main():
    print("Console chatbot (type 'exit' to quit)\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ("exit", "quit"):
            break
        try:
            reply = ask_openrouter(user)
            print("Bot:", reply.strip(), "\n")
        except Exception as e:
            print("Error:", e)
            break

if __name__ == "__main__":
    main()
