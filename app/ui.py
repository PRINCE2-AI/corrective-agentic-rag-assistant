from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.graph import run_query
from app.ingestion import ingest_paths
from app.schemas import QueryRequest, RagMode


st.set_page_config(page_title="Corrective Agentic RAG", layout="wide")
st.title("Corrective Agentic RAG Assistant")
st.caption("CRAG + Adaptive-RAG + RAPTOR-style hierarchy + RAG evaluation")

with st.sidebar:
    st.header("Documents")
    uploads = st.file_uploader(
        "Upload PDF, TXT, or Markdown",
        accept_multiple_files=True,
        type=["pdf", "txt", "md"],
    )
    if uploads and st.button("Ingest documents"):
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        paths = []
        for upload in uploads:
            path = upload_dir / upload.name
            path.write_bytes(upload.getbuffer())
            paths.append(path)
        result = ingest_paths(paths)
        st.success(f"Indexed {result.chunk_count} chunks")

    mode = st.selectbox("Mode", [mode.value for mode in RagMode], index=2)
    use_web = st.checkbox("Allow web correction", value=True)
    simulate_bad = st.checkbox("Simulate retrieval failure", value=False)

question = st.chat_input("Ask a question about your documents")
if question:
    response = run_query(
        QueryRequest(
            question=question,
            mode=RagMode(mode),
            use_web=use_web,
            simulate_bad_retrieval=simulate_bad,
        )
    )
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(response.answer)

    left, right = st.columns(2)
    with left:
        st.subheader("Routing")
        st.metric("Query type", response.query_type.value)
        st.metric("CRAG action", response.action.value)
        st.metric("Confidence", response.confidence)
    with right:
        st.subheader("Evaluation")
        st.json(response.metrics.model_dump())

    st.subheader("Retrieved Chunks")
    for chunk in response.retrieved_chunks[:5]:
        st.caption(f"{chunk.source} | score={chunk.score}")
        st.write(chunk.text)

    st.subheader("Refined Context")
    for chunk in response.refined_context:
        st.caption(f"{chunk.source} | score={chunk.score}")
        st.write(chunk.text)

    if response.web_sources:
        st.subheader("Web Sources")
        for source in response.web_sources:
            st.caption(f"{source.title} | score={source.score}")
            st.write(source.url or source.content)

