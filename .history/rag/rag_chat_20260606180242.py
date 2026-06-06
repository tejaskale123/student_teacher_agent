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
You are a PDF assistant.

IMPORTANT RULES:

1. Answer ONLY from the provided context.
2. Never use outside knowledge.
3. If the answer is not found in the context, reply exactly:

I could not find that information in the PDF.

4. Do not guess.
5. Do not make assumptions.
6. Keep answers clear and concise.

Context:
{context}

Question:
{question}

Answer:
"""

        return self.llm.ask(prompt)