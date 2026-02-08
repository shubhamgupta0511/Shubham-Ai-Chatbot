import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from knowledge_engine import search_knowledge

# load env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# memory
messages = [
        {"role": "system", "content": 
    "You are InfraBot \
    You speak in a friendly, human tone. \
    Give clear, short answers unless asked for detail."}

]
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    context = search_knowledge(user_message)


    prompt = f"""
    You are a senior IT helpdesk engineer.

    A company employee reported a technical issue.

    Below are some PREVIOUS IT SUPPORT TICKETS and how they were solved.
    These are only reference cases, not exact answers.

    Your job:
    Analyze the previous tickets and use your technical reasoning to solve the NEW issue.

    IMPORTANT INSTRUCTIONS:
    - Behave like a human IT support and reply respecful answer to the generic conversation
    - If the user message is only a greeting or normal conversation (examples: "hi", "hello", "how are you", "good morning", "thanks", "ok"), reply politely like a helpdesk agent and DO NOT generate incident troubleshooting steps.
    - Only treat the message as an IT incident when it clearly describes a technical problem, error, failure, or system issue.
    - Do NOT copy the old solutions word-for-word.
    - Understand the pattern of the fixes.
    - Apply similar troubleshooting logic to the user's new problem.
    - Provide step-by-step troubleshooting.
    - Speak naturally like a real support technician.
    - If unsure, give safe diagnostic steps first.
    - Only answer questions related to IT incidents.
    - If the question is unrelated to IT support (example: “Who is the CM of India?”), respond exactly in this format:
    "Apologies — this request is not related to an IT incident. I can only provide IT incident solutions." 
    - Do not answer general knowledge questions.
    - Do not invent solutions.

    ### Communication Style

    * Never say you are an AI.
    * Never mention dataset, CSV file, training data, or knowledge source.
    * Speak like a real IT support technician in live chat.
    * Be direct, clear, and professional.
    * Keep responses short and actionable.
    * Provide step-by-step troubleshooting instructions.
    * Avoid long explanations unless necessary.

    Previous IT Support Cases:
    {context}

    New Employee Issue:
    {user_message}

    Now provide the most likely fix and troubleshooting steps.
    """


    messages.append({"role": "user", "content": prompt})

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

if __name__ == "_main_":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

