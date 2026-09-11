from genai.rag_chain import build_rag_chain

def test_rag_returns_relevant_policy():
    chain = build_rag_chain()
    result = chain.invoke({"query": "What priority is 6 or more potholes?"})
    answer = result["result"].lower()
    assert "high" in answer

def test_rag_grounded_in_source():
    chain = build_rag_chain()
    result = chain.invoke({"query": "What happened on Main St?"})
    sources = result["source_documents"]
    assert len(sources) > 0
    assert any("incident_log" in doc.metadata.get("source", "") for doc in sources)
