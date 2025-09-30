import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("API key not found")
else:
    # Configuração da página
    st.set_page_config(page_title="BioChat - Assistente de Biologia", page_icon="🌱")
    st.title("🌱 BioChat")
    st.write("Seu assistente virtual para estudos em Biologia!")

    # Histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Entrada do usuário
    user_input = st.chat_input("Digite sua pergunta...")

    if user_input:
        try:
            with st.spinner("Gerando resposta..."):
                # Cria o cliente e o chat temporariamente
                client = genai.Client(api_key=api_key)
                chat = client.chats.create(model="gemini-2.0-flash")
                resposta = chat.send_message(user_input)

            # Atualiza histórico
            st.session_state.messages.append({"user": user_input, "bot": resposta.text})
            st.session_state.messages = st.session_state.messages[-15:]
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

    # Botão para limpar histórico
    if st.button("🗑️ Limpar conversa"):
        st.session_state.messages = []
        st.success("Conversa reiniciada!")

    # Exibe histórico
    for msg in st.session_state.messages:
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["user"])
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["bot"])
