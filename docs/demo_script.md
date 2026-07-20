# Demo Script

Use this flow when recording a GitHub demo GIF or explaining the project in interviews.

1. Start the UI with `streamlit run app/ui.py`.
2. Upload `data/sample_docs/sample_ai_notes.md`.
3. Ask: `How does CRAG handle retrieval failure?`
4. Show that the app reports query type, CRAG action, confidence, refined context, and RAG metrics.
5. Toggle retrieval failure simulation and ask the same question again.
6. Explain that the corrective layer catches weak retrieval instead of blindly generating from bad context.
7. Ask: `Summarize the whole document.`
8. Show the long-context route using hierarchical summary retrieval.

Interview one-liner:

> I built this to show the difference between a demo chatbot and a reliable RAG system: it can inspect retrieval quality, adapt strategy, correct context, and measure answer quality.

