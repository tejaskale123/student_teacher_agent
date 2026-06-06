from memory.memory import Memory
from tools.calculator_tool import CalculatorTool
from tools.search_tool import SearchTool
from agents.router import Router
from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class TeacherAgent:

    def __init__(self):
        self.memory = Memory()
        self.calculator = CalculatorTool()
        self.search_tool = SearchTool()
        self.router = Router()
        self.llm = NvidiaClient(NVIDIA_API_KEY)

    def answer(self, question):
        self.memory.save("student", question)

        route = self.router.route(question)

        if route == "calculator":
            result = self.calculator.calculate(question)
            response = f"Answer = {result}"
            self.memory.save("teacher", response)
            return response

        elif route == "search":
            result = self.search_tool.search(question)
            self.memory.save("teacher", result)
            return result

        history = self.memory.get_history()
        context = ""
        for item in history[-10:]:
            context += f"{item['role']}: {item['message']}\n"

        full_prompt = f"""
Previous Conversation:

{context}
Current Question:
{question}

Answer naturally and use the conversation context if relevant.
"""

        response = self.llm.ask(full_prompt)
        self.memory.save("teacher", response)
        return response
