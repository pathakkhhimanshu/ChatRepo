from flask import Flask , request , jsonify, render_template
import requests 
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
print("DEBUG API KEY =", API_KEY)


app = Flask(__name__)

def ask_ai(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = { 
         "Authorization": f"Bearer {API_KEY}",
         "Content-Type": "application/json",
         "HTTP-Referer": "http://localhost",
         "X-Title": "PythonChatbot"
    }

    data = {
        "model": "nousresearch/nous-hermes-2-mistral-7b:free",
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 200
}

    response = requests.post(url, headers=headers, json=data, timeout=20)
    result = response.json()

    if "choices" in result:
         return result["choices"][0]["message"]["content"]
    elif "error" in result:
         return "AI ERROR: " + result["error"].get("message")
    else:
       return "AI returned an unexpected response"


@app.route("/", methods=["GET", "POST"])
def home():
    chat = []
    if request.method == "POST":
        user_msg = request.form.get("message")
        if not user_msg:
          return render_template("page.html", chat=chat)

        ai_msg = ask_ai(user_msg)

        chat.append(("You", user_msg))
        chat.append(("AI", ai_msg))
    return render_template("page.html", chat=chat)

print("API KEY LOADED:", API_KEY[:10] if API_KEY else "NO KEY")

app.run(debug=True)
 