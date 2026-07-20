from app.query_router import classify_query
from app.schemas import QueryType


def test_current_query_routes_to_web_needed():
    assert classify_query("What is the latest RAG paper in 2026?") == QueryType.WEB_NEEDED


def test_compare_query_routes_to_multi_hop():
    assert classify_query("Compare CRAG and Adaptive RAG for enterprise search") == QueryType.MULTI_HOP


def test_summary_query_routes_to_long_context():
    assert classify_query("Summarize the whole document") == QueryType.LONG_CONTEXT

