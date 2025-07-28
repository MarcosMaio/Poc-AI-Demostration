# =============================================================
#  Streamlit - Marketing Workflows Playground
#  v1.0  |  coloca este arquivo na raiz do projeto
# =============================================================
import json
import logging
from datetime import date
from pathlib import Path
import os

import streamlit as st
from streamlit.components.v1 import html

# ---- back-end imports (seus módulos) ------------------------
from agents import Agents
from helpers import clean_agent_output, initialize_llm

logging.basicConfig(level=logging.INFO)

# ----  configuração -----------------------------------------
st.set_page_config(
    page_title="Marketing AI Workflows",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----  estética básica (assets/styles.css é opcional) -------
css_path = Path("assets/styles.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ----  credenciais / modelo ---------------------------------
MODEL_ALIAS   = "gemini/gemini-2.5-pro"      # ou gpt-4o …
API_KEY       = os.getenv("GEMINI_API_KEY") or ""   # use [secrets] no Streamlit Cloud
LLM_CFG       = dict(temperature=0.0, top_p=1)

# ----  inicializa CrewAI apenas uma vez ----------------------
@st.cache_resource(show_spinner=False)
def get_agents_instance():
    llm = initialize_llm(MODEL_ALIAS, API_KEY, LLM_CFG)
    return Agents(llm)

AGENTS = get_agents_instance()
logger = logging.getLogger("streamlit_app")

# =============================================================
#  Funções utilitárias para cada workflow
# =============================================================
def run_campaign_workflow(inputs: dict):
    agent_keys = ["ContentStrategistAgent",
                  "PostPlannerAgent",
                  "ComplianceReviewerAgent"]
    return _kickoff_workflow(agent_keys, inputs)

def run_post_workflow(inputs: dict):
    agent_keys = ["PostContentCreatorAgent",
                  "PostContentComplianceAgent"]
    return _kickoff_workflow(agent_keys, inputs)

def run_doc_health_workflow(inputs: dict):
    agent_keys = ["DocumentHealthAnalyzerAgent",
                  "DocumentHealthComplianceAgent"]
    return _kickoff_workflow(agent_keys, inputs)

def run_brand_brief_workflow(inputs: dict):
    agent_keys = ["WebsiteBrandBriefAgent",
                  "BrandBriefComplianceAgent"]
    return _kickoff_workflow(agent_keys, inputs)

# ---------- wrapper comum -----------------------------------
def _kickoff_workflow(agent_keys, inputs):
    try:
        raw = AGENTS.workflow(agent_keys=agent_keys, inputs=inputs)
        return clean_agent_output(raw)
    except Exception as e:
        logger.error(e)
        st.error(f"Erro ao executar workflow: {e}")
        return None

# =============================================================
#  UI – barra lateral
# =============================================================
with st.sidebar:
    st.image("assets/logo.png", width=160) if Path("assets/logo.png").exists() else None
    st.title("🎯 Workflows")
    selection = st.radio(
        "Escolha um workflow:",
        ("Campaign Planning", "Post Content", "Document Health", "Website Brand Brief"),
    )
    st.markdown("---")
    st.caption("Todos os fluxos usam os agentes definidos em *agents.yaml*.")

# =============================================================
#  UI – área principal
# =============================================================
st.header(f"🧩 {selection}")

if selection == "Campaign Planning":
    with st.form("campaign_form"):
        col1, col2 = st.columns(2)
        subject   = col1.text_input("Subject", value="Agentes de IA e como eles estão mudando o mundo.")
        objective = col2.selectbox("Objective", ["Engajamento", "Conversão", "Brand Awareness"])
        language  = col1.selectbox("Language", ["Portuguese", "English", "Spanish"], index=0)
        platforms = col2.multiselect("Platforms", ["linkedin", "instagram", "blog"], default=["linkedin","instagram","blog"])
        brand     = st.text_area("Brand guidelines (JSON opcional)", height=120)
        submitted = st.form_submit_button("🚀 Gerar Estratégia + Calendário")
    if submitted:
        inputs = {
            "subject": subject,
            "objective": objective,
            "language": language,
            "platforms": platforms,
            "brand": json.loads(brand) if brand else {},
            "current_date": date.today().isoformat(),
        }
        with st.spinner("Executando agentes…"):
            res = run_campaign_workflow(inputs)
        if res:
            st.success("Workflow concluído!")
            st.subheader("Resultado")
            st.json(res, expanded=False)

elif selection == "Post Content":
    with st.form("post_form"):
        topic  = st.text_input("Topic", value="Agentes de IA: O Guia Definitivo Para Aumentar a Sua Produtividade")
        platform = st.selectbox("Platform", ["blog", "linkedin", "instagram"], index=0)
        description = st.text_area("Description", height=120)
        keywords = st.text_area("Keywords (uma por linha)", value="agentes de ia\ninteligência artificial")
        audience = st.text_input("Audience", value="Profissionais curiosos sobre tecnologia e inovação")
        custom   = st.text_area("Custom instructions (opcional)")
        submitted = st.form_submit_button("🚀 Gerar Post + Compliance")
    if submitted:
        inputs = {
            "topic": topic,
            "platform": platform,
            "description": description,
            "keywords": [k.strip() for k in keywords.splitlines() if k.strip()],
            "audience": audience,
            "custom_instructions": custom,
        }
        with st.spinner("Executando agentes…"):
            res = run_post_workflow(inputs)
        if res:
            st.success("Post pronto!")
            st.text_area("Texto final", value=res, height=500)

elif selection == "Document Health":
    with st.form("doc_form"):
        content = st.text_area("Conteúdo (Markdown ou texto)", height=400)
        submitted = st.form_submit_button("🚀 Analisar Saúde do Documento")
    if submitted:
        inputs = {"content_to_analyze": content}
        with st.spinner("Executando agentes…"):
            res = run_doc_health_workflow(inputs)
        if res:
            st.success("Relatório gerado!")
            st.json(res, expanded=False)

elif selection == "Website Brand Brief":
    with st.form("brand_form"):
        url = st.text_input("Website URL", value="https://www.marica.rj.gov.br/")
        submitted = st.form_submit_button("🚀 Gerar Brand Brief")
    if submitted:
        inputs = {"website_url": url}
        with st.spinner("Executando agentes…"):
            res = run_brand_brief_workflow(inputs)
        if res:
            st.success("Brand Brief gerado!")
            st.json(res, expanded=False)

#  Rodapé bonito
st.markdown(
    """
    <hr>
    <center style="font-size:0.8rem">
      Feito com ❤️ e CrewAI • Última atualização: {:%d/%m/%Y}
    </center>
    """.format(date.today()),
    unsafe_allow_html=True,
)
