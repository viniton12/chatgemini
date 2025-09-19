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

    # Estilos customizados para parecer WhatsApp/Telegram
    st.markdown("""
        <style>
        .user-bubble {
            background-color: #DCF8C6;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px;
            max-width: 70%;
            text-align: left;
            float: right;
            clear: both;
        }
        .bot-bubble {
            background-color: #E8E8E8;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px;
            max-width: 70%;
            text-align: left;
            float: left;
            clear: both;
        }
        </style>
    """, unsafe_allow_html=True)

    # Exibe o histórico no estilo chat (bolhas de conversa)
    for msg in st.session_state.messages:
        st.markdown(f"<div class='user-bubble'>👤 {msg['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-bubble'>🤖 {msg['bot']}</div>", unsafe_allow_html=True)

