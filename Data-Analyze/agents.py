import logging
import yaml
from crewai import Agent, Task, Crew, LLM
from crewai.project import agent, task
from tools.generate_analysis_graphics_tool import generate_analysis_graphics_tool

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

    @agent
    def agent(self) -> Agent:
        return Agent(
            config=self.agents_config["Agent"],
            llm=self.llm,
            max_iter=5,
            tools=[generate_analysis_graphics_tool]
        )

    @task
    def task(self) -> Task:
        return Task(
            config=self.tasks_config["AgentTask"],
            agent=self.agent(),
        )

    def call_agent(self) -> Crew:
        return Crew(
            agents=[self.agent()],
            tasks=[self.task()],
            verbose=True,
        )

    def generate_analyze(self, data_to_analyze: dict) -> dict:
        crew_instance = self.call_agent()
        result = crew_instance.kickoff(inputs={"data_to_analyze": data_to_analyze})

        return {
            "pdf_path": result.raw if result.raw else result.json_dict()
        }
