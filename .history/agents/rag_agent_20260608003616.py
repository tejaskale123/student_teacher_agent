from rag.rag_chat import RAGChat


class RAGAgent:

    def __init__(self):
        self.rag = RAGChat()

    def run(self, question):
        return self.rag.ask(question)