# Sample AI Notes

Retrieval-Augmented Generation combines document retrieval with language model generation. A strong RAG system should retrieve relevant evidence, cite sources, and avoid unsupported claims.

Corrective Retrieval Augmented Generation adds a retrieval evaluator that judges whether retrieved documents are useful. If the documents are correct, the system refines them and answers. If they are incorrect, the system can use web search. If they are ambiguous, it can combine local and external evidence.

Adaptive RAG changes the retrieval strategy based on query complexity. Simple factual questions can use shallow retrieval. Multi-hop questions need more context and reranking. Current or recent questions may need web search.

RAPTOR-style retrieval uses hierarchical summaries. A document summary captures broad meaning, section summaries capture medium-level context, and raw chunks provide evidence for citation.

RAG evaluation commonly checks context relevance, answer faithfulness, answer relevance, and citation coverage.

