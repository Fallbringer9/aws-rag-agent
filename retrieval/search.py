from domain.models import Chunk
from ingestion.embedder import generate_embedding
from vectordb.faiss_store import FaissStore


def retrieve_relevant_chunks(
    question: str,
    store: FaissStore,
    top_k: int = 3,
) -> list[Chunk]:
    query_vector = generate_embedding(question)
    return store.search(query_vector, top_k=top_k)