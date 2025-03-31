from dotenv import load_dotenv
load_dotenv()  # Must be called before importing the project modules
import streamlit as st
from pdf_rag import rag_chain

st.title("PDF RAG UI")

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

    with st.chat_message("assistant"):
        stream = rag_chain.invoke({"input": prompt})
        response = st.write(stream["answer"])

    st.session_state.messages.append({"role": "assistant", "content": response})
