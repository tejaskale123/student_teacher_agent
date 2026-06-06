from pdf_reader import read_pdf
from chunker import create_chunks

text = read_pdf("sample.pdf")

chunks = create_chunks(text)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0])
