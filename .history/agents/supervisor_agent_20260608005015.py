from agents.math_agent import MathAgent
from agents.search_agent import SearchAgent
from agents.rag_agent import RAGAgent

from agents.planner_agent import PlannerAgent
from agents.combiner_agent import CombinerAgent
from agents.reflection_agent import ReflectionAgent


class SupervisorAgent:

    def __init__(self):

        self.math_agent = MathAgent()
        self.search_agent = SearchAgent()
        self.rag_agent = RAGAgent()

        self.planner = PlannerAgent()
        self.combiner = CombinerAgent()
        self.reflection = ReflectionAgent()

    def handle(self, route, question):

        planned = self.planner.plan(
            question
        )

        if planned:

            results = {}

            for task in planned:

                if task == "search":

                    results["search"] = (
                        self.search_agent.run(
                            question
                        )
                    )

                elif task == "rag":

                    results["rag"] = (
                        self.rag_agent.run(
                            question
                        )
                    )

            combined = (
                self.combiner.combine(
                    results
                )
            )

            return self.reflection.review(
                combined
            )

        if route == "calculator":

            return self.math_agent.run(
                question
            )

        elif route == "search":

            return self.search_agent.run(
                question
            )

        elif route == "rag":

            return self.rag_agent.run(
                question
            )

        return None