from memory.memory import Memory

class TeacherAgent:

    def __init__(self):
        self.memory = Memory()

    def answer(self, question):

        self.memory.save("student", question)

        question = question.lower()

        if "ai" in question:
            response = "AI means Artificial Intelligence."

        elif "python" in question:
            response = "Python is a popular programming language."

        elif "agent" in question:
            response = "An AI Agent can think, plan and use tools."

        else:
            response = "Sorry, I don't know that yet."

        self.memory.save("teacher", response)

        return response