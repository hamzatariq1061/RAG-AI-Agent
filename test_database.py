
from database.db_manager import (
    document_exists,
    save_document,
    get_all_documents
)
from backend.file_utils import calculate_file_hash

sample_content = b"This is a test document."

file_hash = calculate_file_hash(sample_content)

if not document_exists(file_hash):
    save_document("test.txt", file_hash)
    print("Document saved successfully!")
else:
    print("Duplicate document detected!")

print("\nStored Documents:")
for document in get_all_documents():
    print(document)
