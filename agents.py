import logging
from crewai import Agent, Task, Crew, LLM
from crewai.project import agent, task
import os
import yaml
import glob
# from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
# from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource


logger = logging.getLogger("poc_presentations")


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

    def load_yaml(self, filepath):
        with open(filepath, "r") as f:
            return yaml.safe_load(f)

    # files = glob.glob("knowledge/data/**/*.md", recursive=True)
    # files = [file.replace("knowledge/", "", 1) for file in files]

    # print(f"Found {files} markdown files.")
    # knowledge_source = CrewDoclingSource(file_paths=files)
    
    # with open("knowledge/data/file/search_source.md", "r") as file:
    #     content = file.read()
        
    # knowledge_source = StringKnowledgeSource(content=content)

    @agent
    def get_specific_info_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["GetSpecificInfoAgent"],
            llm=self.llm,
            max_iter=2,
            verbose=True,
            # knowledge_sources=[self.knowledge_source]
        )

    @task
    def get_specific_info_task(self) -> Task:
        return Task(
            config=self.tasks_config["GetSpecificInfoTask"],
            agent=self.get_specific_info_agent(),
        )

    def call_agent(self) -> Crew:
        return Crew(
            agents=[
                self.get_specific_info_agent(),
            ],
            tasks=[
                self.get_specific_info_task(),
            ],
            verbose=True,
            # knowledge_sources=[self.knowledge_source]
        )

    def extract_data(self, detailed_instructions: str, document_content: str):
        crew_instance = self.call_agent()
        result = crew_instance.kickoff(
            inputs={
                "detailed_instructions": detailed_instructions,
                "document_content": document_content,
            }
        )
        return result.raw if result.raw else result.json_dict()
