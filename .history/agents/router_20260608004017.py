import re


class Router:

    def route(self, question):

        question = question.lower().strip()

        if re.fullmatch(
            r"[0-9+\-*/(). ]+",
            question
        ):
            return "calculator"

        search_keywords = [
            "search",
            "latest",
            "news",
            "find",
            "lookup"
        ]

        if any(
            word in question
            for word in search_keywords
        ):
            return "search"

        pdf_keywords = [
            "pdf",
            "document",
            "chapter",
            "notes",
            "summary",
            "summarize"
        ]

        if any(
            word in question
            for word in pdf_keywords
        ):
            return "rag"

        return "knowledge"