class PlannerAgent:

    def plan(self, question):

        normalized_question = question.lower().strip()

        has_comparison = any(
            word in normalized_question
            for word in [
                "compare",
                "comparison",
                "difference"
            ]
        )

        has_pdf_context = any(
            word in normalized_question
            for word in [
                "pdf",
                "document",
                "chapter",
                "notes"
            ]
        )

        has_search_context = any(
            word in normalized_question
            for word in [
                "latest",
                "news",
                "search",
                "find",
                "lookup"
            ]
        )

        if (
            has_comparison
            and has_pdf_context
            and has_search_context
        ):

            search_query = normalized_question
            rag_query = normalized_question

            if " with " in normalized_question:
                left, right = normalized_question.split(" with ", 1)
                rag_query = left
                search_query = right

            cleanup_words = [
                "compare",
                "comparison",
                "difference",
                "between",
                "from pdf",
                "in pdf",
                "pdf",
                "document",
                "search",
                "find",
                "lookup"
            ]

            for word in cleanup_words:
                search_query = search_query.replace(word, " ")
                rag_query = rag_query.replace(word, " ")

            search_query = " ".join(search_query.split())
            rag_query = " ".join(rag_query.split())

            if not search_query:
                search_query = normalized_question

            if not rag_query:
                rag_query = normalized_question

            return {
                "search": search_query,
                "rag": rag_query
            }

        return {}
