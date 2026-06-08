import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from agents.math_agent import MathAgent
from agents.search_agent import SearchAgent
from agents.rag_agent import RAGAgent

from agents.planner_agent import PlannerAgent
from agents.combiner_agent import CombinerAgent
from agents.reflection_agent import ReflectionAgent
from agents.critic_agent import CriticAgent
from agents.formatter_agent import FormatterAgent

class SupervisorAgent:

    def __init__(self):

        self.math_agent = MathAgent()
        self.search_agent = SearchAgent()
        self.rag_agent = RAGAgent()

        self.planner = PlannerAgent()
        self.combiner = CombinerAgent()
        self.reflection = ReflectionAgent()
        self.critic = CriticAgent()
        self.last_run = {}

    def log_run(self, payload):
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)

        with (logs_dir / "agent_runs.jsonl").open("a", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    payload,
                    ensure_ascii=False
                )
            )
            file.write("\n")

    def handle(self, route, question):
        started_at = time.perf_counter()

        planned = self.planner.plan(
            question
        )

        if planned:

            search_query = planned["search"]
            rag_query = planned["rag"]

            with ThreadPoolExecutor() as executor:

                search_future = executor.submit(
                    self.search_agent.run,
                    search_query
                )

                rag_future = executor.submit(
                    self.rag_agent.run,
                    rag_query
                )

                search_result = search_future.result()
                rag_result = rag_future.result()

            results = {
                "search": search_result,
                "rag": rag_result
            }

            combined = (
                self.combiner.combine(
                    results
                )
            )

            reflected = self.reflection.review(
                search_result,
                rag_result
            )

            final_answer = self.critic.critique(
                reflected
            )

            execution_time = round(time.perf_counter() - started_at, 2)
            self.last_run = {
                "query": question,
                "route": "multi",
                "agents": ["SearchAgent", "RAGAgent", "ReflectionAgent", "CriticAgent"],
                "execution_time": execution_time,
                "retrieved_chunks": "PDF result generated"
            }
            self.log_run(
                {
                    **self.last_run,
                    "timestamp": datetime.now().isoformat(timespec="seconds")
                }
            )

            return final_answer

        if route == "calculator":

            result = self.math_agent.run(
                question
            )
            agents = ["MathAgent"]

        elif route == "search":

            result = self.search_agent.run(
                question
            )
            agents = ["SearchAgent"]

        elif route == "rag":

            result = self.rag_agent.run(
                question
            )
            agents = ["RAGAgent"]

        else:
            result = None
            agents = []

        execution_time = round(time.perf_counter() - started_at, 2)
        self.last_run = {
            "query": question,
            "route": route,
            "agents": agents,
            "execution_time": execution_time,
            "retrieved_chunks": "N/A"
        }
        self.log_run(
            {
                **self.last_run,
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }
        )

        return result
