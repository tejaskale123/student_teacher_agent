class ConfidenceAgent:

    def score(self, answer):

        if (
            "could not find"
            in answer.lower()
        ):
            return "Low"

        if len(answer) > 500:
            return "High"

        return "Medium"
