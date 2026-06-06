from pdf_reader import read_pdf
from chunker import create_chunks
from embedding_model import create_embeddings
from vector_store import VectorStore
from retriever import Retriever


text = read_pdf("sample.pdf")

chunks = create_chunks(text)

embeddings = create_embeddings(chunks)

store = VectorStore(embeddings)

retriever = Retriever(
    chunks,
    store
)

results = retriever.retrieve(
    "What are Python functions?"
)

for i, chunk in enumerate(results):

    print("\n")
    print("=" * 50)

    print(f"RESULT {i+1}")

    print("=" * 50)

    print(chunk[:500])