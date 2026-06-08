class QueryRewriterAgent:

    def rewrite(self, query):

        query = query.lower()

        if "python" in query:

            return (
                query
                + " programming language"
            )

        if "ai" in query:

            return (
                query
                + " artificial intelligence"
            )

        return query
