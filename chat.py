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
        "messages": [
            {"role": "user", "content": user_message}
        ]

    }

    response = requests.post(url, headers=headers, json=data, timeout=20)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    elif "error" in result:
        return f"Error: {result['error'].get('message')}"
    else:
        return "Error: Unexpected response from AI service."
    
    @app.route("/")  
    def home():
        return render_template("page.html")
    
    @app.route("/chat", methods=["POST"])
    def chat():
        user_message = request.json.get("message")
    ai_reply = ask_ai(user_message)
    return jsonify({"reply": ai_reply})

app.run(debug=True)
        
 