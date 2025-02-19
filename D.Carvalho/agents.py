import logging
from crewai import Agent, Task, Crew, LLM
from crewai.project import agent, task
import yaml
from crewai.knowledge.source.excel_knowledge_source import ExcelKnowledgeSource
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import sqlite3
import json


logger = logging.getLogger("poc_presentations")

class SQLiteQueryInput(BaseModel):
    query: str = Field(..., description="SQL query to execute")
        
class SQLiteQueryTool(BaseTool):
    name: str = "SQLite Query Tool"
    description: str = "Executes SQL queries on a SQLite database and retrieves table information"
    args_schema: type[BaseModel] = SQLiteQueryInput

    def _run(self, query: str) -> str:
        db_path = "database.db"
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                return str(results)
        except Exception as e:
            return f"Error executing query: {str(e)}"

    def get_table_info(self, db_path: str) -> str:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                table_info = []
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    column_info = [f"- {col[1]}: {col[2]}" for col in columns]
                    table_info.append(f"Table Name: {table_name}\nColumns:\n" + "\n".join(column_info))
                
                return "\n\n".join(table_info)
        except Exception as e:
            return f"Error retrieving table information: {str(e)}"
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
        self.table_info = self.load_json("prompt/tables_data_info.json")
        self.db_overview = self.load_markdown("prompt/db_overview.md")
        self.sqlite_tool = SQLiteQueryTool()

    def load_yaml(self, filepath):
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
        
    def load_json(self, filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    
    def load_markdown(self, filepath):
        with open(filepath, "r") as f:
            return f.read()

    @agent
    def get_query_generator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["QueryGeneratorAgent"],
            llm=self.llm,
            verbose=True,
            cache=False,
            max_iter=2,
        )

    @agent
    def get_database_executor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["DatabaseExecutorAgent"],
            llm=self.llm,
            verbose=True,
            cache=False,
            tools=[self.sqlite_tool],
            max_iter=2,
        )
    
    @agent
    def get_result_formatter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ResultFormatterAgent"],
            llm=self.llm,
            verbose=True,
            cache=False,
            max_iter=2,
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
        self.execute_query_task = Task(
            config=self.tasks_config["DatabaseExecutorTask"],
            agent=self.get_database_executor_agent(),
            context=[
                self.query_generator_task
            ],
        )
        return self.execute_query_task
        
    @task
    def get_result_formatter_task(self) -> Task:
        return Task(
            config=self.tasks_config["ResultFormatterTask"],
            agent=self.get_database_executor_agent(),
            context=[
                self.query_generator_task,
                self.execute_query_task
            ],
        )

    def call_agent(self) -> Crew:
        return Crew(
            agents=[
                self.get_query_generator_agent(),
                self.get_database_executor_agent(),
                self.get_result_formatter_agent()
            ],
            tasks=[
                self.get_generate_query_task(),
                self.get_execute_query_task(),
                self.get_result_formatter_task()
            ],
            verbose=True,
            memory=False,
            context=[
                f"Database Schema:\n{self.table_info}",
                f"Database Overview:\n{self.db_overview}"
            ]
        )

    def extract_answer(self, user_question: str):
        crew_instance = self.call_agent()
        result = crew_instance.kickoff(
            inputs={
                "user_question": user_question,
                "table_info": self.table_info,
                "db_overview": self.db_overview
            }
        )
        
        sql_result = self.query_generator_task.output.raw
        
        return {
            "sql_result": sql_result,
            "full_result": result.raw if result.raw else result.json_dict()
        }
    
