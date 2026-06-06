class CalculatorTool:

    def calculate(self, expression):

        try:
            result = eval(expression)
            return result

        except:
            return "Invalid Calculation"