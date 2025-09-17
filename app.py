import streamlit as st
import os
from google import genai

# Configuração da API
api_key = os.getenv("https://github.com/viniton12/chatgemini/blob/main/app.py")

if not api_key:
    st.error("api key not founded")
else:
    client = genai.Client(api_key=api_key)

    st.title("🤖 Chatbot com Streamlit + Gemini")

    # Entrada do usuário
    user_input = st.text_input("Digite sua mensagem:")

    if st.button("Enviar") and user_input:
        chat = client.chats.create(model="gemini-2.0-flash")
        resposta = chat.send_message(user_input)
        st.markdown(f"**Bot:** {resposta.text}")
