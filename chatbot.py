import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

conversation_history = []

def chat(user_message):
    conversation_history.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # Free model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *conversation_history
        ]
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None

    assistant_message = response.json()["choices"][0]["message"]["content"]
    conversation_history.append({"role": "assistant", "content": assistant_message})
    return assistant_message

print("Chatbot ready! Type 'quit' to exit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    reply = chat(user_input)
    if reply:
        print(f"Bot: {reply}\n")