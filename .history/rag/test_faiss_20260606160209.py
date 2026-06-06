from pdf_reader import read_pdf
from chunker import create_chunks
from embedding_model import create_embeddings
from vector_store import VectorStore

text = read_pdf("sample.pdf")

chunks = create_chunks(text)

embeddings = create_embeddings(chunks)

store = VectorStore(embeddings)

query = "What are Python functions?"

query_embedding = create_embeddings(
    [query]
)[0]

results = store.search(
    query_embedding,
    k=3
)

print("Best Chunks:\n")

for idx in results:

    print("=" * 50)

    print(chunks[idx][:500])

    print("\n")