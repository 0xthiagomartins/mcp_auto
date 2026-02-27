"""UI Streamlit: agente conversacional que busca veículos via MCP."""
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import streamlit as st

from src.application.agent import create_agent, invoke_agent
from src.application.mcp_client import init_mcp_client

init_mcp_client()

st.set_page_config(page_title="Busca de Veículos", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = create_agent()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite o que você está buscando (marca, ano, preço, etc.)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = invoke_agent(
            st.session_state.agent,
            prompt,
            st.session_state.messages[:-1],
        )
        st.markdown(response or "Desculpe, ocorreu um erro.")
    st.session_state.messages.append({"role": "assistant", "content": response})
