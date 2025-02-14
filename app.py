import streamlit as st
import os
import json
import shutil
import logging

from agents import Agents
from helpers import (
    process_file,
    clean_agent_output,
    get_detailed_instructions_from_file,
    get_doc_content_from_file
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("poc_presentations")

st.title("POC: Extração de Informações")
st.markdown("""
Esta aplicação permite extrair informações de um documento PDF utilizando diferentes modelos de linguagem por meio de agentes de IA.
""")

st.markdown("""
Selecione o modelo, ajuste os parâmetros e faça o upload do seu arquivo para iniciar o processamento.
""")

st.header("Configurações do Agente")

selected_model = st.selectbox("Selecione o modelo:", options=["gemini-1.5-flash", "gpt-4o", "o1-preview"])

model = f"gemini/{selected_model}" if selected_model == "gemini-1.5-flash" else selected_model

temperature = st.number_input("Temperatura", min_value=0.0, max_value=1.0, value=0.01, step=0.05)
top_p = st.number_input("Top P", min_value=0.0, max_value=1.0, value=0.85, step=0.05)

st.header("Upload do Documento")
uploaded_file = st.file_uploader("Envie o documento (PDF)", type=["pdf"])

if uploaded_file:
    if uploaded_file.type != "application/pdf":
        st.error("Por favor, envie um arquivo PDF válido.")
    else:
        folder_path = "file_to_read"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    st.error(f"Erro ao remover arquivo antigo: {e}")

        file_path = os.path.join(folder_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Arquivo salvo com sucesso!")

        try:
            process_file()
            st.info("Processamento do arquivo realizado com sucesso.")
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
            
        if st.button("Extrair Informações"):
            try:
                detailed_instructions = get_detailed_instructions_from_file()
                document_content = get_doc_content_from_file()

                if model.startswith("gemini"):
                    api_key = os.getenv("GEMINI_API_KEY")
                if model.startswith("gpt") or model == "o1-preview":
                    api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    st.error("API Key não encontrada. Verifique a variável de ambiente.")
                else:
                    agent = Agents(model, api_key, temperature, top_p)
                    st.info("Extraindo informações do documento. Aguarde...")

                    raw_result = agent.extract_data(detailed_instructions, document_content)
                    result = clean_agent_output(raw_result)

                    st.markdown("### Resultado da Extração")
                    try:
                        formatted_result = json.dumps(result, indent=4, ensure_ascii=False)
                        st.code(formatted_result, language='json')
                    except Exception as e:
                        st.error(f"Erro ao formatar o JSON: {e}")
                        st.text(result)
            except Exception as e:
                st.error(f"Erro durante a extração: {e}")
