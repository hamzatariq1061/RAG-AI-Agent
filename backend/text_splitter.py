
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(pages):

    documents = []

    for page in pages:
        documents.append(
            Document(
                page_content=page["text"],
                metadata={
                    "source": page["source"],
                    "page": page["page"]
                }
            )
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks
