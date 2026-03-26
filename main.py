from ingestion.chunker import chunk_document
from ingestion.loader import load_txt_documents
from dotenv import load_dotenv
import os
from ingestion.embedder import embed_chunks
from vectordb.faiss_store import FaissStore
from agent.rag_agent import create_rag_agent


load_dotenv()

AWS_PROFILE = os.getenv("AWS_PROFILE")
AWS_REGION = os.getenv("AWS_REGION")


def main():
    documents = load_txt_documents("data/docs")
    store = FaissStore()
    print(f"Loaded {len(documents)} documents")

    total_chunks = 0

    for doc in documents:
        chunks = chunk_document(doc)

        if chunks:
            embedded = embed_chunks(chunks)
            store.add(embedded)
            total_chunks += len(chunks)

    print(f"Indexed {total_chunks} chunks")

    print("\n==== AGENT TEST ====\n")
    query = "What is AWS Lambda?"

    agent = create_rag_agent(store)
    response = agent(query)

    print(f"Question: {query}\n")
    print("Answer:")
    print(response)



if __name__ == "__main__":
    main()