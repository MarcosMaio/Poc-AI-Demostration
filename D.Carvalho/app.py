import streamlit as st
import os
import logging

from agents import Agents 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("poc_presentations")

st.title("POC: Extração de Consultas no Banco de Dados")
st.markdown("""
Esta aplicação permite que você consulte um banco de dados utilizando linguagem natural.
Digite sua pergunta abaixo (mínimo 10 caracteres) e clique em "Executar Consulta" para obter a resposta.
""")

st.header("Configurações do Agente")
selected_model = st.selectbox("Selecione o modelo:", options=["gemini-1.5-flash", "gpt-4o", "o1-preview"])
model = f"gemini/{selected_model}" if selected_model == "gemini-1.5-flash" else selected_model
temperature = st.number_input("Temperatura", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
top_p = st.number_input("Top P", min_value=0.0, max_value=1.0, value=0.85, step=0.05)

if model.startswith("gpt") or model == "o1-preview":
    api_key = os.getenv("OPENAI_API_KEY")
elif model.startswith("gemini"):
    api_key = os.getenv("GEMINI_API_KEY")
else:
    api_key = None

if not api_key:
    st.error("API Key não encontrada. Por favor, defina a variável de ambiente apropriada.")
    st.stop()

st.header("Digite sua Pergunta")
user_question = st.text_input("Sua pergunta:", "")

if user_question and len(user_question.strip()) < 10:
    st.error("A pergunta deve conter no mínimo 10 caracteres.")

if st.button("Executar Consulta") and user_question and len(user_question.strip()) >= 10:
    st.info("Processando sua consulta. Aguarde...")
    try:
        agent_instance = Agents(model, api_key, temperature, top_p)
        result = agent_instance.extract_answer(user_question)
        
        st.markdown("### Resposta da Consulta")
        st.text_area("Resposta", value=str(result), height=400)
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a consulta: {e}")
