import re

from config import NVIDIA_API_KEY
from llm.nvidia_client import NvidiaClient


class Router:

    def __init__(self):
        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def route(self, question):

        question = question.lower().strip()

        if re.fullmatch(
            r"[0-9+\-*/(). ]+",
            question
        ):
            return "calculator"

        if re.search(
            r"\d+\s*[+\-*/]\s*\d+",
            question
        ):
            print("\nROUTER CHOICE:")
            print("math")
            return "calculator"

        comparison_keywords = [
            "compare",
            "comparison",
            "difference"
        ]

        search_keywords = [
            "search",
            "latest",
            "news",
            "find",
            "lookup"
        ]

        pdf_keywords = [
            "pdf",
            "document",
            "chapter",
            "notes",
            "summary",
            "summarize"
        ]

        knowledge_starters = [
            "what is",
            "what are",
            "who is",
            "why is",
            "explain",
            "teach me",
            "how does",
            "how to",
            "define",
            "meaning of"
        ]

        has_comparison = any(
            word in question
            for word in comparison_keywords
        )

        has_search_need = any(
            word in question
            for word in search_keywords
        )

        has_pdf_need = any(
            word in question
            for word in pdf_keywords
        )

        has_knowledge_start = any(
            question.startswith(starter)
            for starter in knowledge_starters
        )

        if (
            has_comparison
            and has_search_need
            and has_pdf_need
        ):
            print("\nROUTER CHOICE:")
            print("multi")
            return "multi"

        if has_search_need:
            print("\nROUTER CHOICE:")
            print("search")
            return "search"

        if has_pdf_need:
            print("\nROUTER CHOICE:")
            print("rag")
            return "rag"

        if has_knowledge_start:
            print("\nROUTER CHOICE:")
            print("knowledge")
            return "knowledge"

        knowledge_keywords = [
            "what is",
            "explain",
            "define",
            "meaning"
        ]

        has_knowledge_keyword = any(
            keyword in question
            for keyword in knowledge_keywords
        )

        if has_knowledge_keyword:
            print("\nROUTER CHOICE:")
            print("knowledge")
            return "knowledge"

        try:
            prompt = f"""
You are an AI Router.

Available Agents:

search
rag
math
knowledge

Question:
{question}

Rules:

- Return ONLY agent names.
- No explanation.
- No code.
- No sentences.
- No markdown.

Examples:

Question: latest ai news
Answer: search

Question: what is 10+10
Answer: math

Question: what is python
Answer: knowledge

Question: summarize chapter 1
Answer: rag

Question: compare python functions from pdf with latest python news
Answer: search,rag

Return only the answer.
"""
            route = self.llm.ask(prompt)
            route = route.strip().lower()

            print("\nROUTER CHOICE:")
            print(route)

            valid_routes = [
                "search",
                "rag",
                "math",
                "knowledge",
                "search,rag"
            ]

            if route not in valid_routes:
                route = "knowledge"

            if route == "search,rag":
                return "multi"

            if route == "math":
                return "calculator"

            if route == "search":
                return "search"

            if route == "rag":
                return "rag"

            if route == "knowledge":
                return "knowledge"

        except Exception as error:
            print("\nROUTER LLM FALLBACK:")
            print(error)

        if any(
            word in question
            for word in comparison_keywords
        ):
            return "multi"

        if any(
            word in question
            for word in search_keywords
        ):
            return "search"

        if any(
            word in question
            for word in pdf_keywords
        ):
            return "rag"

        return "knowledge"
