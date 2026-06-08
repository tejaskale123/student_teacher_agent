import json
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
from agents.answer_generator_agent import AnswerGeneratorAgent
from agents.search_summarizer_agent import SearchSummarizerAgent
from agents.confidence_agent import ConfidenceAgent
from agents.execution_monitor_agent import ExecutionMonitor

class SupervisorAgent:

    def __init__(self):

        self.math_agent = MathAgent()
        self.search_agent = SearchAgent()
        self.rag_agent = RAGAgent()

        self.planner = PlannerAgent()
        self.combiner = CombinerAgent()
        self.reflection = ReflectionAgent()
        self.critic = CriticAgent()
        self.formatter = FormatterAgent()
        self.answer_generator = AnswerGeneratorAgent()
        self.search_summarizer = SearchSummarizerAgent()
        self.confidence = ConfidenceAgent()
        self.monitor = ExecutionMonitor()
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
        self.monitor.start()

        planned = self.planner.plan(
            question
        )

        if route == "multi" and not planned:
            planned = {
                "search": question,
                "rag": question
            }

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

            search_result = (
                self.search_summarizer
                .summarize(
                    search_result
                )
            )

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
                rag_result,
                combined
            )

            final_answer = self.critic.critique(
                reflected
            )

            formatted_answer = self.formatter.format(
                final_answer
            )

            generated_answer = self.answer_generator.generate(
                formatted_answer
            )

            confidence_score = self.confidence.score(
                generated_answer
            )
            execution_time = self.monitor.stop()
            print("Confidence Score:", confidence_score)
            print(f"Execution Time: {execution_time} sec")

            self.last_run = {
                "query": question,
                "route": "multi",
                "agents": ["SearchAgent", "QueryRewriterAgent", "SearchSummarizerAgent", "RAGAgent", "ReflectionAgent", "CriticAgent", "FormatterAgent", "AnswerGeneratorAgent", "ConfidenceAgent", "ExecutionMonitor"],
                "execution_time": execution_time,
                "confidence": confidence_score,
                "retrieved_chunks": "PDF result generated"
            }
            self.log_run(
                {
                    **self.last_run,
                    "timestamp": datetime.now().isoformat(timespec="seconds")
                }
            )

            return generated_answer

        if route == "calculator":

            result = self.math_agent.run(
                question
            )
            agents = ["MathAgent"]

        elif route == "search":

            result = self.search_agent.run(
                question
            )
            result = (
                self.search_summarizer
                .summarize(
                    result
                )
            )
            agents = ["SearchAgent", "SearchSummarizerAgent"]
            execution_time = self.monitor.stop()
            print("Confidence Score: High")
            print(f"Execution Time: {execution_time} sec")
            self.last_run = {
                "query": question,
                "route": route,
                "agents": agents + ["ExecutionMonitor"],
                "execution_time": execution_time,
                "confidence": "High",
                "retrieved_chunks": "N/A"
            }
            self.log_run(
                {
                    **self.last_run,
                    "timestamp": datetime.now().isoformat(timespec="seconds")
                }
            )
            return result

        elif route == "rag":

            result = self.rag_agent.run(
                question
            )
            agents = ["RAGAgent"]

        else:
            result = None
            agents = []

        if result is not None:
            formatted_result = self.formatter.format(
                result
            )

            result = self.answer_generator.generate(
                formatted_result
            )
            agents = agents + ["FormatterAgent", "AnswerGeneratorAgent"]

            confidence_score = self.confidence.score(
                result
            )
            agents = agents + ["ConfidenceAgent"]
        else:
            confidence_score = "Low"

        execution_time = self.monitor.stop()
        print("Confidence Score:", confidence_score)
        print(f"Execution Time: {execution_time} sec")
        agents = agents + ["ExecutionMonitor"]

        self.last_run = {
            "query": question,
            "route": route,
            "agents": agents,
            "execution_time": execution_time,
            "confidence": confidence_score,
            "retrieved_chunks": "N/A"
        }
        self.log_run(
            {
                **self.last_run,
                "timestamp": datetime.now().isoformat(timespec="seconds")
            }
        )

        return result
