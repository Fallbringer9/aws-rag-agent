import json
import os
from typing import Any

from app.ingestion_service import run_ingestion_pipeline


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        if not bucket_name:
            raise ValueError("BUCKET_NAME is not set")

        result = run_ingestion_pipeline(bucket_name)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(result),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "error": str(e),
            }),
        }