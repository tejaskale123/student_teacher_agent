from agents.rag_agent import RAGAgent


class SupervisorAgent:

    def __init__(self):

        self.rag_agent = RAGAgent()

    def handle(self, route, question):

        if route == "rag":
            return self.rag_agent.run(question)

        return None