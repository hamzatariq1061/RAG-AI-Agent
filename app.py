
import streamlit as st
from pathlib import Path
from uuid import uuid4
from html import escape

from backend.document_loader import load_multiple_documents
from backend.text_splitter import split_documents
from backend.vector_store import create_vector_store
from backend.rag_chain import ask_question
from backend.file_utils import calculate_file_hash

from database.db_manager import (
    document_exists,
    save_document,
    get_all_documents
)

# ----------------------------------------
# APP CONFIGURATION
# ----------------------------------------

st.set_page_config(
    page_title="NEXUS AI | Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------
# CUSTOM CSS
# ----------------------------------------

css_path = Path(__file__).parent / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

# ----------------------------------------
# SESSION STATE
# ----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed_count" not in st.session_state:
    st.session_state.processed_count = 0

# ----------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------

def render_sources(sources):
    if not sources:
        return

    with st.expander("📚 View Sources"):
        seen = set()

        for source in sources:
            name = source.get("source", "Unknown")
            page = source.get("page")

            key = (name, page)

            if key in seen:
                continue

            seen.add(key)

            if page is not None:
                st.markdown(
                    f"📄 **{name}** — Page {page}"
                )
            else:
                st.markdown(f"📄 **{name}**")


def process_uploaded_documents(uploaded_files):
    if not uploaded_files:
        st.warning("Please select documents first.")
        return

    new_files = []
    skipped = 0
    seen_hashes = set()

    try:
        with st.spinner(
            "Reading documents and building knowledge base..."
        ):
            for uploaded_file in uploaded_files:
                file_bytes = uploaded_file.getvalue()

                file_hash = calculate_file_hash(
                    file_bytes
                )

                if (
                    file_hash in seen_hashes
                    or document_exists(file_hash)
                ):
                    skipped += 1
                    continue

                seen_hashes.add(file_hash)

                safe_name = Path(uploaded_file.name).name
                unique_name = (
                    f"{uuid4().hex}_{safe_name}"
                )

                file_path = UPLOAD_DIR / unique_name
                file_path.write_bytes(file_bytes)

                new_files.append(
                    (file_path, file_hash, safe_name)
                )

            if not new_files:
                st.info(
                    "All selected documents are already indexed."
                )
            else:
                pages = load_multiple_documents(
                    [item[0] for item in new_files]
                )

                chunks = split_documents(pages)

                if not chunks:
                    st.error(
                        "No readable text was found "
                        "in the selected documents."
                    )
                else:
                    create_vector_store(chunks)

                    for path, file_hash, filename in new_files:
                        save_document(filename, file_hash)

                    st.session_state.processed_count += len(
                        new_files
                    )

                    st.success(
                        f"{len(new_files)} document(s) indexed "
                        f"successfully!"
                    )

                    st.caption(
                        f"{len(chunks)} text chunks added."
                    )

            if skipped:
                st.warning(
                    f"{skipped} duplicate document(s) skipped."
                )

    except Exception as error:
        st.error(f"Processing failed: {error}")


# ----------------------------------------
# SIDEBAR
# ----------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-title">NEXUS AI</div>
                <div class="brand-subtitle">
                    KNOWLEDGE INTELLIGENCE
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-label">DOCUMENT WORKSPACE</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload knowledge files",
        type=["pdf", "docx", "odt", "txt"],
        accept_multiple_files=True,
        max_upload_size=20,
        help="Upload multiple files, up to 20 MB each."
    )

    if st.button(
        "✦ Process Documents",
        type="primary",
        use_container_width=True
    ):
        process_uploaded_documents(uploaded_files)

    st.markdown(
        '<div class="section-label">KNOWLEDGE BASE</div>',
        unsafe_allow_html=True
    )

    documents = get_all_documents()

    if documents:
        st.caption(
            f"{len(documents)} indexed document(s)"
        )

        for doc_id, filename, uploaded_at in documents:
            safe_filename = escape(str(filename))
            safe_date = escape(str(uploaded_at))

            st.markdown(
                f"""
                <div class="file-card">
                    <div class="file-name">
                        📄 {safe_filename}
                    </div>
                    <div class="file-date">
                        Added {safe_date}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Your knowledge base is empty.")

    st.divider()

    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "Powered by OpenAI · LangChain · FAISS"
    )

# ----------------------------------------
# MAIN DASHBOARD
# ----------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">
            ✦ INTELLIGENT DOCUMENT SEARCH
        </div>
        <div class="hero-title">
            Your knowledge, amplified.
        </div>
        <div class="hero-description">
            Ask questions, discover insights and get
            grounded answers from your documents.
            All in one intelligent workspace.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

documents = get_all_documents()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Indexed Documents</div>
            <div class="stat-value">{len(documents)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">Chat Messages</div>
            <div class="stat-value">
                {len(st.session_state.messages)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-label">AI Engine</div>
            <div class="stat-value"
                 style="font-size:19px;margin-top:14px">
                ● OpenAI
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# ----------------------------------------
# CHAT SECTION
# ----------------------------------------

st.subheader("💬 AI Knowledge Chat")

if not st.session_state.messages:
    st.info(
        "Welcome to NEXUS AI. Upload documents in "
        "the sidebar, then ask your first question."
    )

    st.markdown("**Try asking:**")

    suggestions = [
        "Summarize the uploaded documents",
        "Explain the main concepts",
        "What are the key findings?"
    ]

    cols = st.columns(3)

    for col, suggestion in zip(cols, suggestions):
        with col:
            if st.button(
                suggestion,
                use_container_width=True
            ):
                st.session_state.pending_question = suggestion
                st.rerun()

# ----------------------------------------
# DISPLAY MESSAGES
# ----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("sources"):
            render_sources(message["sources"])

# ----------------------------------------
# QUESTION INPUT
# ----------------------------------------

typed_question = st.chat_input(
    "Ask anything about your documents..."
)

pending_question = st.session_state.pop(
    "pending_question",
    None
)

question = typed_question or pending_question

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your knowledge base..."):
            try:
                result = ask_question(question)

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)
                render_sources(sources)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as error:
                st.error(
                    f"Unable to generate answer: {error}"
                )
