
from pathlib import Path
from langchain_community.vectorstores import FAISS

from backend.embeddings import get_embeddings

DB_PATH = Path("faiss_index")


def create_vector_store(chunks):
    if not chunks:
        raise ValueError("No text chunks available.")

    embeddings = get_embeddings()

    if DB_PATH.exists():
        vector_store = FAISS.load_local(
            str(DB_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(
            chunks,
            embeddings
        )

    vector_store.save_local(str(DB_PATH))

    return vector_store


def load_vector_store():
    if not DB_PATH.exists():
        return None

    return FAISS.load_local(
        str(DB_PATH),
        get_embeddings(),
        allow_dangerous_deserialization=True
    )
