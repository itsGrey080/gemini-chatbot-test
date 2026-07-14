from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

st.title("Avinav's Chat App")

API_KEY = Path(__file__).parent.joinpath("apikey").read_text().strip()

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash"
SYSTEM_PROMPT = "You are a helpful assistant from Nepal that can answer questions in nepali and help with tasks."    


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
query = st.chat_input("enter any query")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    gemini_history = [
        types.Content(
            role="user" if m["role"] == "user" else "model",
            parts=[types.Part(text=m["content"])],
        )
        for m in st.session_state.messages
    ]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=gemini_history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.5,
        ),
    )

    full_response = response.text

    with st.chat_message("assistant"):
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})


