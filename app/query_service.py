from typing import Any

from agent.rag_agent import create_rag_agent
from domain.models import Chunk
from vectordb.artifact_store import download_artifacts, load_metadata
from vectordb.faiss_store import FaissStore


def deserialize_chunks(metadata: list[dict[str, Any]]) -> list[Chunk]:
    chunks: list[Chunk] = []

    for item in metadata:
        chunks.append(
            Chunk(
                chunk_id=item["chunk_id"],
                source=item["source"],
                text=item["text"],
            )
        )

    return chunks


def run_query_pipeline(question: str, bucket_name: str) -> dict[str, Any]:
    index_path, metadata_path = download_artifacts(bucket_name)

    metadata = load_metadata(metadata_path)
    chunks = deserialize_chunks(metadata)

    store = FaissStore.load(index_path, chunks)
    agent = create_rag_agent(store)
    answer = agent(question)

    return {
        "question": question,
        "answer": str(answer),
        "sources": [chunk.chunk_id for chunk in chunks],
        "bucket_name": bucket_name,
    }
