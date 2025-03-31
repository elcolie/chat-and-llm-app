import streamlit as st
import random
import time
from openai import OpenAI

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets["general"]["OPENAI_API_KEY"])

# Streamed response emulator
def response_generator():
    response = random.choice([
        "Hello! How can I help you today?",
        "I'm here to assist you. What do you need?",
        "Hi there! What can I do for you?",
        "Greetings! How may I assist you?",
        "Hey! What would you like to know?",
    ])
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            stream=True,
        )

        response = st.write_stream(stream)
    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
