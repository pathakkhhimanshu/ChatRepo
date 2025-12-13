from flask import Flask, request 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form.get("message")
        print("user said:", user_message)
        return "Message received"
    
    return """
             <h2>Simple Chat Test</h2>
        <form method="post">
            <input type="text" name="message" placeholder="Type something">
            <button type="submit">Send</button>
        </form>
    """
app.run(debug=True)