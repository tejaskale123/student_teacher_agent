from agents.math_agent import MathAgent
from agents.search_agent import SearchAgent
from agents.rag_agent import RAGAgent


class SupervisorAgent:

    def __init__(self):

        self.math_agent = MathAgent()
        self.search_agent = SearchAgent()
        self.rag_agent = RAGAgent()

    def handle(self, route, question):

        if route == "calculator":
            return self.math_agent.run(question)

        elif route == "search":
            return self.search_agent.run(question)

        elif route == "rag":
            return self.rag_agent.run(question)

        return None