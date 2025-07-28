import logging
from pathlib import Path
from typing import Any, cast
import os

import yaml
from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool, WebsiteSearchTool , ScrapeWebsiteTool
from langchain_openai import OpenAIEmbeddings   


logger = logging.getLogger("jedai")

TOOL_REGISTRY: dict[str, BaseTool] = {
    "search_web":  SerperDevTool(),
    "search_site": WebsiteSearchTool( 
        embeddings=OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    ),
    "scrape_website": ScrapeWebsiteTool(), 
}
class Agents:
    def __init__(self, llm):
        self.llm = llm
        cfg_dir = Path("config")
        if not cfg_dir.exists() or not cfg_dir.is_dir():
            logger.error(f"Config directory does not exist or is not a directory: {cfg_dir}")
            raise RuntimeError(f"Config directory does not exist or is not a directory: {cfg_dir}")
        try:
            self.agents_config = self._load_yaml(cfg_dir / "agents.yaml")
            self.tasks_config = self._load_yaml(cfg_dir / "tasks.yaml")
        except FileNotFoundError as e:
            logger.error(f"Could not load AI config: {e}")
            raise RuntimeError("Could not load AI config") from e

    def _load_yaml(self, path: Path) -> dict:
        with open(path) as f:
            data = yaml.safe_load(f)
        logger.info(f"Loaded config: {path.name}")
        return data

    def _build_agent(self, key: str, inputs: dict[str, Any]) -> Agent:
        cfg = self.agents_config[key].copy()
        role = cfg.pop("role")
        goal = cfg.pop("goal")
        backstory = cfg.pop("backstory")
        for exp in cfg.pop("expected_input", []):
            if exp not in inputs:
                raise KeyError(f"Missing expected input '{exp}' for {key}")
        tools = []
        for tname in cfg.pop("tools", []):
            fn = TOOL_REGISTRY.get(tname)
            if not fn:
                raise KeyError(f"Tool '{tname}' not found")
            tools.append(fn)
        params = {}
        raw = cfg.pop("parameters", {})
        if isinstance(raw, list):
            for d in raw:
                if isinstance(d, dict):
                    params.update(d)
        elif isinstance(raw, dict):
            params = raw
        ag_kwargs = {"role": role, "goal": goal, "backstory": backstory, "config": cfg, "llm": self.llm}
        if tools:
            ag_kwargs["tools"] = tools
        for k, v in params.items():
            ag_kwargs[k] = int(v) if isinstance(v, (str,)) and v.isdigit() else v
        return Agent(**ag_kwargs)

    def _build_tasks(self, agent_keys: list[str], inputs: dict[str, Any]) -> dict[str, Task]:
        task_map: dict[str, Task] = {}
        for key in agent_keys:
            agent = self._build_agent(key, inputs)
            tcfg = self.tasks_config[key + "Task"].copy()
            desc = tcfg.pop("description")
            exp = tcfg.pop("expected_output")
            task_map[key] = Task(description=desc, expected_output=exp, config=tcfg, agent=agent, context=None)
        return task_map

    def workflow(
        self,
        agent_keys: list[str],
        inputs: dict[str, Any],
        include_manager: bool = False,
        manager_key: str = "ManagerAgent",
    ) -> Any:
        task_map = self._build_tasks(agent_keys, inputs)

        for key, task in task_map.items():
            depends = self.tasks_config[key + "Task"].get("depends_on", [])
            if depends:
                task.context = [task_map[dep] for dep in depends]
        agents = [task.agent for task in task_map.values()]
        tasks = list(task_map.values())
        crew_kwargs = {"agents": agents, "tasks": tasks, "verbose": True}

        if include_manager:
            mgr = self._build_agent(manager_key, inputs)
            crew_kwargs.update({"manager_agent": mgr, "manager_llm": self.llm, "process": Process.hierarchical})
        crew = Crew(**crew_kwargs)
        res = crew.kickoff(inputs=inputs)

        if res is None:
            logger.error("crew.kickoff() returned None.")
            raise RuntimeError("crew.kickoff() returned None.")

        if hasattr(res, "raw") and getattr(res, "raw"):
            return getattr(res, "raw")
        elif hasattr(res, "json_dict"):
            json_dict_attr = getattr(res, "json_dict")
            if callable(json_dict_attr):
                return json_dict_attr()
            elif isinstance(json_dict_attr, dict):
                return json_dict_attr
            else:
                logger.error("crew.kickoff() returned an object with 'json_dict' that is neither callable nor a dict.")
                raise RuntimeError(
                    "crew.kickoff() returned an object with 'json_dict' that is neither callable nor a dict."
                )
        else:
            logger.error("crew.kickoff() returned an unexpected result without 'raw' or 'json_dict'.")
            raise RuntimeError("crew.kickoff() returned an unexpected result without 'raw' or 'json_dict'.")
