from rag.rag_chat import RAGChat


class RAGAgent:

    def __init__(self):
        self.rag = None

    def run(self, question):
        print("RAG START")

        if self.rag is None:
            self.rag = RAGChat()

        result = self.rag.ask(question)

        print("\n=== RAG RESULT ===")
        print(result[:300])

        return result
