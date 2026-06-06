from pdf_reader import read_pdf

text = read_pdf("sample.pdf")

print(text[:1000])