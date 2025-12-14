from flask import Flask, request 
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
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "LearningChatbot"
}


    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        result = response.json()

        print("FULL AI RESPONSE:", result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        elif "error" in result:
            return f"AI ERROR: {result['error'].get('message')}"

        else:
            return "AI returned an unexpected response."

    except Exception as e:
        return f"REQUEST FAILED: {e}"



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_message = request.form.get("message")

        ai_reply = ask_ai(user_message)
        print("AI replied:", ai_reply)

        return ai_reply   

    return """
        <h2>AI Chat Test</h2>
        <form method="post">
            <input type="text" name="message">
            <button type="submit">Send</button>
        </form>
    """

app.run(debug=True)


 