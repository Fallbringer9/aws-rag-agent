import boto3
import json
import os

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("BEDROCK_REGION", "us-east-1")
)


def generate_text_response(prompt: str) -> str:
    response = bedrock.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt,
                    }
                ],
            }
        ],
        inferenceConfig={
            "maxTokens": 300,
            "temperature": 0.7,
        },
    )

    return response["output"]["message"]["content"][0]["text"]