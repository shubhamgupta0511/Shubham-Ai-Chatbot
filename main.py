import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("\nShubham's AI")
print("Type 'exit' to quit\n")

# conversation memory
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye 👋")
        break

    # store user message
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=400,
        )

        reply = response.choices[0].message.content

        print("\nAI:", reply, "\n")

        # store AI reply
        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Error:", e)
