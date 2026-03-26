import faiss
import numpy as np

from domain.models import Chunk


class FaissStore:
    def __init__(self, dimension: int = 1024):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.chunks: list[Chunk] = []

    def add(self, embedded_chunks: list[tuple[Chunk, list[float]]]) -> None:
        if not embedded_chunks:
            return

        vectors: list[list[float]] = []
        chunks_to_add: list[Chunk] = []

        for chunk, vector in embedded_chunks:
            if len(vector) != self.dimension:
                raise ValueError(
                    f"Embedding dimension mismatch: expected {self.dimension}, got {len(vector)}"
                )

            chunks_to_add.append(chunk)
            vectors.append(vector)

        vectors_array = np.array(vectors, dtype="float32")
        self.index.add(vectors_array)
        self.chunks.extend(chunks_to_add)

    def save(self, path: str) -> None:
        """Save the FAISS index to a local file."""
        faiss.write_index(self.index, path)

    def search(self, query_vector: list[float], top_k: int = 3) -> list[Chunk]:
        if len(query_vector) != self.dimension:
            raise ValueError(
                f"Query vector dimension mismatch: expected {self.dimension}, got {len(query_vector)}"
            )

        if self.index.ntotal == 0:
            return []

        query_array = np.array([query_vector], dtype="float32")
        _, indices = self.index.search(query_array, top_k)

        results: list[Chunk] = []

        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.chunks[idx])

        return results

    @classmethod
    def load(cls, path: str, chunks: list[Chunk], dimension: int = 1024) -> "FaissStore":
        """Load a FAISS index from a local file and reattach the chunk metadata."""
        store = cls(dimension=dimension)
        store.index = faiss.read_index(path)
        store.chunks = chunks
        return store