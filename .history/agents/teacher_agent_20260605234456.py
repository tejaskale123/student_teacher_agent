from memory.memory import Memory
from tools.calculator_tool import CalculatorTool
from tools.search_tool import SearchTool
from agents.router import Router
from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY
from config import NVIDIA_API_KEY

class TeacherAgent:

    def __init__(self):
        self.nvidia_client = NvidiaClient(NVIDIA_API_KEY)

        self.memory = Memory()

        self.calculator = CalculatorTool()

        self.search_tool = SearchTool()

        self.router = Router()

    def answer(self, question):

        self.memory.save("student", question)

        route = self.router.route(question)

        # Calculator Route
        if route == "calculator":

            result = self.calculator.calculate(question)

            response = f"Answer = {result}"

            self.memory.save("teacher", response)

            return response

        # Search Route
        elif route == "search":

            result = self.search_tool.search(question)

            response = result

            self.memory.save("teacher", response)

            return response

        # Knowledge Route
        question = question.lower()

        if "ai" in question:

            response = "AI means Artificial Intelligence."

        elif "python" in question:

            response = "Python is a popular programming language."

        elif "agent" in question:

            response = "An AI Agent can think, plan and use tools."

        else:

            response = self.llm.ask(question)

        self.memory.save("teacher", response)

        return response