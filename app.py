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

    # Configuração da página
    st.set_page_config(page_title="BioChat - Assistente de Biologia", page_icon="🌱")
    st.title("🌱 BioChat")
    st.write("Seu assistente virtual para estudos em Biologia!")

    # Inicializa o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat" not in st.session_state:
        st.session_state.chat = client.chats.create(model="gemini-2.0-flash")

    # Entrada do usuário
    user_input = st.chat_input("Digite sua pergunta...")

    if user_input:
        try:
            with st.spinner("Gerando resposta..."):
                resposta = st.session_state.chat.send_message(user_input)

            # Adiciona ao histórico
            st.session_state.messages.append({"user": user_input, "bot": resposta.text})

            # Limita histórico para últimas 15 mensagens
            st.session_state.messages = st.session_state.messages[-15:]
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

    # Botão para limpar histórico
    if st.button("🗑️ Limpar conversa"):
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(model="gemini-2.0-flash")
        st.success("Conversa reiniciada!")

    # Exibe o histórico no estilo chat
    for msg in st.session_state.messages:
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["user"])
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["bot"])
