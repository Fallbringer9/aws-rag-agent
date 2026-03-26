from pathlib import Path

from domain.models import Document


def load_txt_documents(directory: str) -> list[Document]:
    documents: list[Document] = []

    docs_path = Path(directory)

    for file_path in docs_path.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                source=file_path.name,
                text=text,
            )
        )

    return documents