class IntentAgent:

    def detect(self, question):
        question = (
            question
            .lower()
            .strip()
        )

        if (
            "full form" in question
        ):
            return "short_answer"

        if (
            "exam" in question
            or "2 marks" in question
            or "5 marks" in question
            or "unit" in question
        ):
    return "exam"

        elif (
            "interview" in question
            or "job" in question
        ):
            return "interview"

        elif (
            "compare" in question
        ):
            return "comparison"

        elif (
            "research" in question
        ):
            return "research"

        return "general"
