
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from odf.opendocument import load
from odf import teletype

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".odt", ".txt"}


def load_document(file_path):
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file: {extension}")

    pages = []

    if extension == ".pdf":
        reader = PdfReader(str(file_path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if text.strip():
                pages.append({
                    "text": text,
                    "source": file_path.name,
                    "page": page_number
                })

    elif extension == ".docx":
        document = Document(str(file_path))
        text = "\n".join(
            p.text for p in document.paragraphs
            if p.text.strip()
        )

        pages.append({
            "text": text,
            "source": file_path.name,
            "page": None
        })

    elif extension == ".odt":
        document = load(str(file_path))
        text = teletype.extractText(document.text)

        pages.append({
            "text": text,
            "source": file_path.name,
            "page": None
        })

    elif extension == ".txt":
        text = file_path.read_text(encoding="utf-8-sig")

        pages.append({
            "text": text,
            "source": file_path.name,
            "page": None
        })

    return [
        page for page in pages
        if page["text"].strip()
    ]


def load_multiple_documents(file_paths):
    all_pages = []

    for file_path in file_paths:
        pages = load_document(file_path)
        all_pages.extend(pages)

    return all_pages
