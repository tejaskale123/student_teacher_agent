from rag.pdf_reader import read_pdf, read_pdfs_from_folder
from rag.chunker import create_chunks
from rag.embedding_model import create_embeddings
from rag.vector_store import VectorStore
from rag.retriever import Retriever

from llm.nvidia_client import NvidiaClient
from config import NVIDIA_API_KEY
import os
import pickle
from pathlib import Path


def get_available_pdf_paths():
    pdf_paths = []

    for folder in ("pdfs", "uploads/pdfs"):
        folder_path = Path(folder)

        if folder_path.exists():
            pdf_paths.extend(
                sorted(folder_path.glob("*.pdf"))
            )

    return pdf_paths


def pdfs_are_newer_than_cache(cache_paths):
    pdf_paths = get_available_pdf_paths()

    if not pdf_paths:
        return False

    if not all(
        Path(cache_path).exists()
        for cache_path in cache_paths
    ):
        return True

    newest_pdf_time = max(
        pdf_path.stat().st_mtime
        for pdf_path in pdf_paths
    )

    oldest_cache_time = min(
        Path(cache_path).stat().st_mtime
        for cache_path in cache_paths
    )

    return newest_pdf_time > oldest_cache_time

class RAGChat:

   def __init__(self):

    store = VectorStore()

    # Load existing files if available
    cache_paths = [
        "chunks.pkl",
        "faiss_index.bin"
    ]

    if (
        os.path.exists("chunks.pkl")
        and os.path.exists("faiss_index.bin")
        and not pdfs_are_newer_than_cache(cache_paths)
    ):

        print("Loading Saved Chunks...")

        with open(
            "chunks.pkl",
            "rb"
        ) as f:

            self.chunks = pickle.load(f)

        print("Loading Saved FAISS...")

        store.load(
            "faiss_index.bin"
        )

    else:

        print("Loading PDFs...")

        text = read_pdfs_from_folder(
            "pdfs"
        )

        if not text.strip():
            text = read_pdfs_from_folder(
                "uploads/pdfs"
            )

        if not text.strip():
            text = read_pdf(
                "sample.pdf"
            )

        print("Creating Chunks...")

        self.chunks = create_chunks(
            text
        )

        with open(
            "chunks.pkl",
            "wb"
        ) as f:

            pickle.dump(
                self.chunks,
                f
            )

        print("Creating Embeddings...")

        embeddings = create_embeddings(
            self.chunks
        )

        print("Building FAISS Index...")

        store = VectorStore(
            embeddings
        )

        store.save(
            "faiss_index.bin"
        )

        print("FAISS Saved!")

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
        k=3
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

Context:
{context}

Question:
{question}

Answer:
"""

    answer = self.llm.ask(prompt)

    return answer
