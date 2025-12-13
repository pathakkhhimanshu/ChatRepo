from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Chat Application!"

app.run(debug=True)