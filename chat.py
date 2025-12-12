import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise SystemExit("OPENROUTER_API_KEY not found. Add it to .env")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "X-Api-Key": API_KEY,
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


#     import os
# import requests
# from dotenv import load_dotenv
# import json

# load_dotenv()
# API_KEY = os.getenv("OPENROUTER_API_KEY")

# print("OPENROUTER_API_KEY found?", bool(API_KEY))
# if API_KEY:
#     # show a masked key (first/last 4 chars)
#     show = f"{API_KEY[:4]}...{API_KEY[-4:]}" if len(API_KEY) > 8 else API_KEY
#     print("API key (masked):", show)

# API_URL = "https://openrouter.ai/api/v1/chat/completions"

# HEADERS = {
#     "X-Api-Key": API_KEY,           # REQUIRED header
#     "Content-Type": "application/json",
#     # Remove referer if you suspect it might be blocked:
#     # "HTTP-Referer": "http://localhost",
#     "X-Title": "MyChatbot"
# }

# payload = {
#     "model": "meta-llama/llama-3.1-8b-instruct:free",
#     "messages": [{"role": "user", "content": "hello"}],
#     "max_tokens": 16,
#     "temperature": 0.7
# }

# print("\n--- REQUEST ---")
# print("URL:", API_URL)
# print("HEADERS:", json.dumps({k: (v if k!="X-Api-Key" else show) for k,v in HEADERS.items()}, indent=2))
# print("BODY:", json.dumps(payload, indent=2))

# try:
#     resp = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
#     print("\n--- RESPONSE ---")
#     print("status_code:", resp.status_code)
#     # server error message / body
#     print("text:", resp.text)
#     # debug: show what headers were actually sent (requests PreparedRequest)
#     prepared = resp.request
#     print("\n--- SENT (prepared request) ---")
#     print("sent headers:", dict(prepared.headers))
#     # printed body (may be bytes)
#     print("sent body length:", len(prepared.body) if prepared.body else 0)
# except Exception as e:
#     print("Exception during request:", repr(e))

