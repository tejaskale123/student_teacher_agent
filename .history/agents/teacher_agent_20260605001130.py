from memory.memory import Memory
from tools.calculator_tool import CalculatorTool
from tools.search_tool import SearchTool

class TeacherAgent:

    def __init__(self):

        self.memory = Memory()

        self.calculator = CalculatorTool()

        self.search_tool = SearchTool()

    def answer(self, question):

        self.memory.save("student", question)

        # Calculator Tool
        if any(op in question for op in ["+", "-", "*", "/"]):

            result = self.calculator.calculate(question)

            response = f"Answer = {result}"

            self.memory.save("teacher", response)

            return response

        question = question.lower()

        if "ai" in question:

            response = "AI means Artificial Intelligence."

        elif "python" in question:

            response = "Python is a popular programming language."

        elif "agent" in question:

            response = "An AI Agent can think, plan and use tools."

        else:

            response = "Sorry, I don't know that yet."

        self.memory.save("teacher", response)

        return response