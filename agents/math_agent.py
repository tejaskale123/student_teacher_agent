from tools.calculator_tool import CalculatorTool


class MathAgent:

    def __init__(self):
        self.calculator = CalculatorTool()

    def run(self, question):
        return self.calculator.calculate(question)