import json
import os
from typing import Any

from app.query_service import run_query_pipeline


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        bucket_name = os.getenv("BUCKET_NAME")
        if not bucket_name:
            raise ValueError("BUCKET_NAME is not set")

        body = event.get("body")
        if not body:
            raise ValueError("Missing request body")

        data = json.loads(body)
        question = data.get("question")

        if not question:
            raise ValueError("Missing 'question' field in request body")

        result = run_query_pipeline(question, bucket_name)

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