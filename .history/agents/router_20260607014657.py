class Router:

    def route(self, question):

        question = question.lower().strip()

        # Calculator
        if any(op in question for op in ["+", "-", "*", "/"]):
            return "calculator"

        # Search
        search_keywords = [
            "search",
            "latest",
            "news",
            "find",
            "lookup"
        ]

        if any(word in question for word in search_keywords):
            return "search"

        # PDF / RAG
        pdf_keywords = [
            "pdf",
            "document",
            "chapter",
            "notes",
            "summary",
            "summarize",
            "what are python",
            "python function",
            "python functions",
            "for loop",
            "while loop",
            "class in python",
            "classes in python"
        ]

        if any(word in question for word in pdf_keywords):
            return "rag"

        return "knowledge"