from pdf_reader import read_pdf
from chunker import create_chunks
from embedding_model import create_embeddings

text = read_pdf("sample.pdf")

chunks = create_chunks(text)

embeddings = create_embeddings(chunks)

print("Total Chunks:", len(chunks))
print("Total Embeddings:", len(embeddings))

print("\nEmbedding Shape:")
print(embeddings.shape)