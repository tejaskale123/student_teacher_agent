class TeacherAgent:

    def answer(self, question):

        question = question.lower()

        if "ai" in question:
            return "AI means Artificial Intelligence."

        elif "python" in question:
            return "Python is a popular programming language."

        elif "agent" in question:
            return "An AI Agent can think, plan and use tools."

        else:
            return "Sorry, I don't know that yet."