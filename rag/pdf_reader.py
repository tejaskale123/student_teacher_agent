from pypdf import PdfReader
from pathlib import Path


def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def read_pdfs_from_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        return ""

    text_parts = []

    for pdf_path in sorted(folder.glob("*.pdf")):
        pdf_text = read_pdf(pdf_path)

        if pdf_text.strip():
            text_parts.append(
                f"\n\nSOURCE PDF: {pdf_path.name}\n{pdf_text}"
            )

    return "\n\n".join(text_parts)
