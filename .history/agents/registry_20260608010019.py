from agents.search_agent import SearchAgent
from agents.math_agent import MathAgent
from agents.rag_agent import RAGAgent
from agents.research_agent import ResearchAgent


class AgentRegistry:

    def __init__(self):

        self.agents = {

            "search": SearchAgent(),

            "math": MathAgent(),

            "rag": RAGAgent(),

            "research": ResearchAgent()
        }

    def get_agent(self, name):

        return self.agents.get(name)