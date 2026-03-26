import boto3
import os
import json

from domain.models import Chunk

session = boto3.Session(
    profile_name=os.getenv("AWS_PROFILE"),
    region_name=os.getenv("BEDROCK_REGION", "us-east-1"),
)

bedrock_client = session.client("bedrock-runtime")

def generate_embedding(text: str):
    body = json.dumps({
        "inputText": text
    })

    response = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())

    embedding = response_body["embedding"]

    return embedding


def embed_chunks(chunks: list[Chunk]) -> list[tuple[Chunk, list[float]]]:
    embedded_chunks: list[tuple[Chunk, list[float]]] = []

    for chunk in chunks:
        vector = generate_embedding(chunk.text)
        embedded_chunks.append((chunk, vector))

    return embedded_chunks