

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