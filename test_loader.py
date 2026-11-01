
from backend.document_loader import load_document

file_path = "storage/uploads/sample.pdf"

pages = load_document(file_path)

print("Total extracted pages:", len(pages))

for page in pages[:2]:
    print("\nDocument:", page["source"])
    print("Page:", page["page"])
    print("Text:", page["text"][:500])
