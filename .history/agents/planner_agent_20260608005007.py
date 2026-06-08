class PlannerAgent:

    def plan(self, question):

        question = question.lower()

        tasks = []

        if any(
            word in question
            for word in [
                "compare",
                "comparison",
                "difference"
            ]
        ):

            tasks.append("search")
            tasks.append("rag")

            return tasks

        return []