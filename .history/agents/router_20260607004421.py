class Router:

    def route(self, question):

        question = question.lower()

        if any(op in question for op in ["+", "-", "*", "/"]):
            return "calculator"

        if "search" in question:
            return "search"

        pdf_keywords = [
            "pdf",
            "document",
            "chapter",
            "notes",
            "summary",
            "summarize"
        ]

        if any(word in question for word in pdf_keywords):
            return "rag"

        return "knowledge"