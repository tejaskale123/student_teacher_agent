from rag.pdf_reader import read_pdf
from rag.chunker import create_chunks
from rag.embedding_model import create_embeddings
from rag.vector_store import VectorStore
from rag.retriever import Retriever

from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY
import os
import pickle

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
            question,
            k=5
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
5. Keep answers short and clear.
6. If possible, explain in simple language.

Context:
{context}

Question:
{question}

Answer:
"""

        answer = self.llm.ask(prompt)

        return answer