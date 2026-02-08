import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# load env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# memory
messages = [
        {"role": "system", "content": 
    "You are Shubham's personal AI assistant. \
    You speak in a friendly, human tone. \
    Give clear, short answers unless asked for detail."}

]
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=400,
        )

        reply = response.choices[0].message.content

        messages.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
