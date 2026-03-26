from dataclasses import dataclass

@dataclass
class Document:
    source: str
    text: str

@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str