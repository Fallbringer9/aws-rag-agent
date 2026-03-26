import typing
from typing import Any

from domain.models import Chunk
from ingestion.chunker import chunk_document
from ingestion.embedder import embed_chunks
from ingestion.s3_loader import load_txt_documents_from_s3
from vectordb.artifact_store import save_metadata, upload_artifacts
from vectordb.faiss_store import FaissStore
from typing import Any

import boto3

from domain.models import Document


s3_client = boto3.client("s3")


def load_txt_documents_from_s3(bucket: str, prefix: str = "documents/") -> list[Document]:
    documents: list[Document] = []

    paginator = s3_client.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            key = item["Key"]

            if key.endswith("/") or not key.endswith(".txt"):
                continue

            response = s3_client.get_object(Bucket=bucket, Key=key)
            body: Any = response["Body"].read()
            text = body.decode("utf-8")

            documents.append(
                Document(
                    source=key,
                    text=text,
                )
            )

    return documents

INDEX_LOCAL_PATH = "/tmp/index.faiss"
METADATA_LOCAL_PATH = "/tmp/metadata.json"


def serialize_chunks(chunks: list[Chunk]) -> list[dict[str, Any]]:
    metadata: list[dict[str, Any]] = []

    for chunk in chunks:
        metadata.append(
            {
                "chunk_id": chunk.chunk_id,
                "source": chunk.source,
                "text": chunk.text,
            }
        )

    return metadata


def run_ingestion_pipeline(bucket_name: str) -> dict[str, Any]:
    documents = load_txt_documents_from_s3(bucket_name)

    all_chunks: list[Chunk] = []

    for document in documents:
        chunks = chunk_document(document)
        all_chunks.extend(chunks)

    embedded_chunks = embed_chunks(all_chunks)

    store = FaissStore()
    store.add(embedded_chunks)
    store.save(INDEX_LOCAL_PATH)

    metadata = serialize_chunks(all_chunks)
    save_metadata(METADATA_LOCAL_PATH, metadata)

    upload_artifacts(
        bucket=bucket_name,
        index_path=INDEX_LOCAL_PATH,
        metadata_path=METADATA_LOCAL_PATH,
    )

    return {
        "documents_indexed": len(documents),
        "chunks_indexed": len(all_chunks),
        "bucket_name": bucket_name,
        "index_s3_key": "artifacts/index.faiss",
        "metadata_s3_key": "artifacts/metadata.json",
    }
