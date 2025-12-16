from flask import Flask , request , render_template
import requests 
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"Loaded API Key: {API_KEY[:20]}..." if API_KEY else "No key loaded!")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not loaded")


app = Flask(__name__)

def ask_ai(user_message):
    print(f"ask_ai called with: {user_message}") 
    url =  f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    headers = { 
         "Content-Type": "application/json"
    }

    data =  {"contents": [{"parts": [{"text": user_message}]}]}
    
    print(f"Making request to: {url[:80]}...")
    response = requests.post(url, headers=headers, json=data, timeout=20)
    result = response.json()
     
    print(f"Status Code: {response.status_code}")  
    print(f"Full Response: {result}")

    if "candidates" in result:
         return result["candidates"][0]["content"]["parts"][0]["text"]
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

if __name__ == "__main__":
    app.run(debug=True)      #
 