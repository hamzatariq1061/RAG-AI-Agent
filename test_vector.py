
from backend.document_loader import load_document
from backend.text_splitter import split_documents
from backend.vector_store import create_vector_store

pages = load_document("storage/uploads/sample.pdf")

chunks = split_documents(pages)

print("Total chunks:", len(chunks))
print("Generating OpenAI embeddings...")

vector_store = create_vector_store(chunks)

print("FAISS database created successfully!")

results = vector_store.similarity_search(
    "What is Machine Learning?",
    k=3
)

for i, doc in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Source:", doc.metadata.get("source"))
    print("Page:", doc.metadata.get("page"))
    print("Text:", doc.page_content[:300])
