import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# Carrega a API key do .env
load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("API key not found")
else:
    client = genai.Client(api_key=api_key)

    st.title("🤖 Chatbot com Streamlit + Gemini")

    user_input = st.text_input("Digite sua mensagem:")

    if st.button("Enviar") and user_input:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            messages=[{"role": "user", "content": user_input}]
        )
        resposta = chat.messages[-1].content
        st.markdown(f"**Bot:** {resposta}")
