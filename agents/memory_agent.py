from memory.memory import Memory


class MemoryAgent:

    def __init__(self):

        self.memory = Memory()

    def get_context(self):

        history = self.memory.get_history()

        context = ""

        for item in history[-10:]:

            context += (
                f"{item['role']}: "
                f"{item['message']}\n"
            )

        return context