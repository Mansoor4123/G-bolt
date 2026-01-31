import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# This line looks for the .env file and loads your key automatically
load_dotenv()

# Get the key from the environment
api_key = os.environ.get("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

st.set_page_config(page_title="G-Bolt", layout="centered")
st.title("⚡ G-Bolt")

# --- Rest of your chat code remains exactly the same ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=True,
        )

        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_response += content
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})