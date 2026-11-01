
from backend.document_loader import load_document
from backend.text_splitter import split_documents

pages = load_document("storage/uploads/sample.pdf")

chunks = split_documents(pages)

print("Total Pages:", len(pages))
print("Total Chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3], start=1):
    print(f"\n--- Chunk {i} ---")
    print("Source:", chunk.metadata["source"])
    print("Page:", chunk.metadata["page"])
    print("Text:", chunk.page_content[:300])
