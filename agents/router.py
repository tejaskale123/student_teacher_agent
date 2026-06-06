class Router:

    def route(self, question):

        question = question.lower()

        if any(op in question for op in ["+", "-", "*", "/"]):
            return "calculator"

        if "search" in question:
            return "search"

        return "knowledge"