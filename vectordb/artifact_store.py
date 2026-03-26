

import os
import json
from typing import Tuple

import boto3


s3_client = boto3.client("s3")


# ---------- Low-level helpers ----------

def upload_file(local_path: str, bucket: str, key: str) -> None:
    """Upload a local file to S3."""
    s3_client.upload_file(local_path, bucket, key)


def download_file(bucket: str, key: str, local_path: str) -> None:
    """Download a file from S3 to a local path."""
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3_client.download_file(bucket, key, local_path)


# ---------- Artifact helpers ----------

ARTIFACTS_PREFIX = "artifacts"
INDEX_FILENAME = "index.faiss"
METADATA_FILENAME = "metadata.json"


def upload_artifacts(bucket: str, index_path: str, metadata_path: str) -> None:
    """Upload FAISS index and metadata to S3 under the artifacts/ prefix."""
    upload_file(index_path, bucket, f"{ARTIFACTS_PREFIX}/{INDEX_FILENAME}")
    upload_file(metadata_path, bucket, f"{ARTIFACTS_PREFIX}/{METADATA_FILENAME}")


def download_artifacts(bucket: str, base_dir: str = "/tmp") -> Tuple[str, str]:
    """Download FAISS index and metadata from S3 into base_dir.

    Returns:
        (index_local_path, metadata_local_path)
    """
    index_local_path = os.path.join(base_dir, INDEX_FILENAME)
    metadata_local_path = os.path.join(base_dir, METADATA_FILENAME)

    download_file(bucket, f"{ARTIFACTS_PREFIX}/{INDEX_FILENAME}", index_local_path)
    download_file(bucket, f"{ARTIFACTS_PREFIX}/{METADATA_FILENAME}", metadata_local_path)

    return index_local_path, metadata_local_path


# ---------- Metadata helpers ----------

def save_metadata(local_path: str, data: list[dict]) -> None:
    """Save metadata JSON locally."""
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_metadata(local_path: str) -> list[dict]:
    """Load metadata JSON from local path."""
    with open(local_path, "r", encoding="utf-8") as f:
        return json.load(f)