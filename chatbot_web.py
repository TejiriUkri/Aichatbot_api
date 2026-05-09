import os
import requests
import streamlit as st

# Page config
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.caption("Powered by Groq + Llama")

# Load API key from Streamlit secrets
API_KEY = st.secrets["GROQ_API_KEY"]
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# Initialize conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display chat history on screen
for message in st.session_state.conversation_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to send message to Groq
def chat(user_message):
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_message
    })

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.conversation_history
        ]
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    assistant_message = response.json()["choices"][0]["message"]["content"]
    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

# Chat input box at the bottom
if user_input := st.chat_input("Type your message here..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Show bot reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chat(user_input)
        st.markdown(reply)