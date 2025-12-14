from flask import Flask , request , jsonify, render_template
import requests 
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

def ask_ai(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = { 
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://Localhost:5000",
        "X-Title": "LearningChatbot"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": user_message}]
}

    response = requests.post(url, headers=headers, json=data,)
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def home():
    chat = []
    if request.method == "POST":
        user_msg = request.form.get("message")
        ai_msg = ask_ai(user_msg)
        chat.append(("You", user_msg))
        chat.append(("AI", ai_msg))
    return render_template("page.html", chat=chat)

app.run(debug=True)
 