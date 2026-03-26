from domain.models import Chunk, Document


def chunk_document(
    document: Document,
    chunk_size: int = 300,
    overlap: int = 50,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    text = document.text.strip()

    if not text:
        return chunks

    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                Chunk(
                    chunk_id=f"{document.source}_{chunk_index}",
                    source=document.source,
                    text=chunk_text,
                )
            )

        chunk_index += 1
        start += chunk_size - overlap

    return chunks