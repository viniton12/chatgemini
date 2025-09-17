import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# Carrega a API key do .env
load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

# Inicializa o cliente
if not api_key:
    st.error("API key not found")
else:
    client = genai.Client(api_key=api_key)

    st.set_page_config(page_title="Chatbot AI", page_icon="🤖")
    st.title("🤖 Biochat")
    st.write("Estou aqui para ajudar!!.")

    # Inicializa o histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Entrada do usuário
    user_input = st.text_area("Sua mensagem:", height=100)

    if st.button("Enviar") and user_input:
        try:
            # Cria o chat e envia a mensagem
            chat = client.chats.create(model="gemini-2.0-flash")
            resposta = chat.send_message(user_input)

            # Adiciona ao histórico
            st.session_state.messages.append({"user": user_input, "bot": resposta.text})

            # Limita histórico para as últimas 15 mensagens
            st.session_state.messages = st.session_state.messages[-15:]
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

    # Exibe o histórico de mensagens
    for msg in st.session_state.messages:
        st.markdown(f"**Você:** {msg['user']}")
        st.markdown(f"**Bot:** {msg['bot']}")
        st.markdown("---")
