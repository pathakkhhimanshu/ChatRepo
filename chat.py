from flask import Flask , request , jsonify, render_template
import requests 
import os 
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not loaded")


app = Flask(__name__)

def ask_ai(user_message):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    headers = { 
         "Authorization": f"Bearer {API_KEY}",
         "Content-Type": "application/json",
         "HTTP-Referer": "http://localhost",
         "X-Title": "PythonChatbot"
    }

    data = {
        "model": "gemini-2.5-flash:generateContent",
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


app.run(debug=True)
 