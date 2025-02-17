import logging
from crewai import Agent, Task, Crew, LLM
from crewai.project import agent, task
import os
import yaml
import glob
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import sqlite3


logger = logging.getLogger("poc_presentations")

class SQLiteQueryInput(BaseModel):
    query: str = Field(..., description="SQL query to execute")
    db_path: str = Field("database.db", description="Path to the SQLite database")

class SQLiteQueryTool(BaseTool):
    name: str = "SQLite Query Tool"
    description: str = "Executes SQL queries on a SQLite database"
    args_schema: type[BaseModel] = SQLiteQueryInput

    def _run(self, query: str, db_path: str) -> str:
        try:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                return str(results)
        except Exception as e:
            return f"Error executing query: {str(e)}"

class Agents:
    def __init__(self, model: str, api_key: str, temperature: float, top_p: float):
        self.llm = LLM(
            model=model,
            api_key=api_key,
            temperature=temperature,
            top_p=top_p,
        )

        self.agents_config = self.load_yaml("config/agents.yaml")
        self.tasks_config = self.load_yaml("config/tasks.yaml")
        
        
        self.sqlite_tool = SQLiteQueryTool()
        
        self.table_info = (
            "Table Name: produtos\n"
            "Description: Tabela contendo informações sobre os produtos disponíveis, incluindo estoque, preços, últimas compras e vendas.\n"
            "Columns:\n"
            "- FILIAL: TEXT\n"
            "- CodigoProduto: TEXT\n"
            "- DescricaoProduto: TEXT\n"
            "- Modelo: TEXT\n"
            "- ModeloDescricao: TEXT\n"
            "- Grupo_John_Deere: TEXT\n"
            "- UnidadeMedida: TEXT\n"
            "- Marca: TEXT\n"
            "- EstoqueDisponivel: REAL\n"
            "- EstoqueReservaBalcao: REAL\n"
            "- EstoqueReservaOficina: REAL\n"
            "- PrecoVenda: REAL\n"
            "- CustoMedioUnitario: REAL\n"
            "- ValorUltimaCompraFilial: REAL\n"
            "- Locacao: TEXT\n"
            "- UltimaCompraFilial: TEXT\n"
            "- UltimaCompra: TEXT\n"
            "- UltimaVendaFilial: TEXT\n"
            "- UltimaVenda: TEXT\n"
            "- DataInclusao: TEXT\n"
            "- UsuarioInclusao: TEXT\n"
            "- DataAlteracao: TEXT\n"
            "- UsuarioAlteracao: TEXT\n"
        )

    def load_yaml(self, filepath):
        with open(filepath, "r") as f:
            return yaml.safe_load(f)

    # files = glob.glob("knowledge/data/files/*.xlsx")
    # files = [file.replace("knowledge/", "", 1) for file in files]
    # print(f"Found ({files}) files.")
    
    # excel_source = ExcelKnowledgeSource(
    #     file_paths=files
    # )

    @agent
    def get_query_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["QueryGeneratorAgent"],
            llm=self.llm,
            verbose=True,
            cache=False,
        )

    @agent
    def get_database_interaction_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["DatabaseExpertAgent"],
            llm=self.llm,
            verbose=True,
            cache=False,
            tools=[self.sqlite_tool],
        )

    @task
    def get_generate_query_task(self) -> Task:
        self.query_generator_task = Task(
            config=self.tasks_config["QueryGeneratorTask"],
            agent=self.get_query_generator_agent(),
        )
        return self.query_generator_task
        
    @task
    def get_execute_query_task(self) -> Task:
        return Task(
            config=self.tasks_config["DatabaseExpertTask"],
            agent=self.get_database_interaction_agent(),
            context=[
                self.query_generator_task
            ],
        )

    def call_agent(self) -> Crew:
        return Crew(
            agents=[
                self.get_query_generator_agent(),
                self.get_database_interaction_agent()
            ],
            tasks=[
                self.get_generate_query_task(),
                self.get_execute_query_task()
            ],
            verbose=True,
            memory=False,
        )

    def extract_answer(self, user_question: str):
        crew_instance = self.call_agent()
        result = crew_instance.kickoff(
            inputs={
                "user_question": user_question,
                "table_info": self.table_info
            }
        )
        return result.raw if result.raw else result.json_dict()
