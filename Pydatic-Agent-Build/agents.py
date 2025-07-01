import yaml, json
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic import BaseModel
class Agents:
    def __init__(self, model: str, api_key: str, temperature: float, top_p: float):
        # load your YAML configs
        cfg = yaml.safe_load(open("config/agents.yaml"))
        task_cfg = yaml.safe_load(open("config/tasks.yaml"))

        gemini = GeminiModel(
            model, 
            provider=GoogleGLAProvider(api_key=api_key)
        )
        
        class ExtractionOutput(BaseModel):
            emissorId: str
            codigoExterno: str
            numeroEmissao: int
            numeroSerie: str

        
        self.agent = Agent(
            gemini,
            system_prompt=self._make_system_prompt(cfg["GetSpecificInfoAgent"]),
            temperature=temperature,
            top_p=top_p,
            output_type=ExtractionOutput,
        )

        self.task_description = task_cfg["GetSpecificInfoTask"]["description"]

    def _make_system_prompt(self, agent_cfg: dict) -> str:
        return "\n\n".join([
            agent_cfg["role"],
            agent_cfg["goal"],
            agent_cfg["backstory"],
        ])

    def extract_data(self, detailed_instructions: str, document_content: str) -> dict:
        prompt = self.task_description.format(
            detailed_instructions=detailed_instructions,
            document_content=document_content,
        )
        result = self.agent.run_sync(prompt)

        # result.output is an ExtractionOutput instance
        return result.output.dict()