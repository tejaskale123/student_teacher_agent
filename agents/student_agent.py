from agents.teacher_agent import TeacherAgent

class StudentAgent:

    def __init__(self):
        self.teacher = TeacherAgent()

    def ask_teacher(self, question):
        return self.teacher.answer(question)