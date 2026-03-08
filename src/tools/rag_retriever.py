from typing import List

class MockDocument:
    def __init__(self, content: str, source: str):
        self.page_content = content
        self.metadata = {"source": source}

def retrieve_travel_blogs(query: str, k: int = 3) -> List[MockDocument]:
    """
    Simulates a Vector Database RAG Retrieval for Hyper-Personalization.
    In a real application, this would use FAISS/ChromaDB + LangChain embeddings
    loaded from local travel blog PDFs to find "hidden gems".
    """
    hidden_gems = [
        MockDocument(
            content="If you go to Tokyo, skip the crowded parts of Shibuya and find the tiny hidden izakayas in Omoide Yokocho.", 
            source="tokyo_secrets.pdf"
        ),
        MockDocument(
            content="In Bali, avoid Kuta beach and instead rent a scooter to explore the waterfalls in Munduk for a serene experience.", 
            source="bali_nomad_guide.md"
        ),
        MockDocument(
            content="The best time to see the Eiffel tower is actually at 1 AM when the lights sparkle one last time with no crowds.",
            source="paris_travel_blog.txt"
        ),
        MockDocument(
            content="The absolute best budget tacos in Mexico City are found at a small cart near the Coyoacan market.",
            source="cdmx_foodie.md"
        )
    ]
    
    # Simple semantic search mock
    results = []
    for doc in hidden_gems:
        # Very crude word matching for demo purposes
        if any(word.lower() in doc.page_content.lower() for word in query.split()):
            results.append(doc)
            
    # Fallback if no specific matches
    if not results:
        results = hidden_gems[:k]
        
    return results[:k]
