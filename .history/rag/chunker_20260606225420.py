from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(text):
    # Handle list of dicts from pdf_reader
    if isinstance(text, list):
        text = "\n".join([item.get("text", "") for item in text])
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)
    return chunks
