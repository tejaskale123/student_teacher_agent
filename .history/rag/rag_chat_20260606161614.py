from pdf_reader import read_pdf
from chunker import create_chunks
from embedding_model import create_embeddings
from vector_store import VectorStore
from retriever import Retriever

from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY


class RAGChat:

    def __init__(self):

        print("Loading PDF...")

        text = read_pdf("sample.pdf")

        print("Creating Chunks...")

        self.chunks = create_chunks(text)

        print("Creating Embeddings...")

        embeddings = create_embeddings(
            self.chunks
        )

        print("Building FAISS Index...")

        store = VectorStore(
            embeddings
        )

        self.retriever = Retriever(
            self.chunks,
            store
        )

        self.llm = NvidiaClient(
            NVIDIA_API_KEY
        )

    def ask(self, question):

        docs = self.retriever.retrieve(
            question
        )

        context = "\n\n".join(docs)

        prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{question}
"""

        return self.llm.ask(prompt)