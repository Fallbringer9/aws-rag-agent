from retrieval.search import retrieve_relevant_chunks


def retrieval_tool(question: str, store):
    """
    Tool used by the agent to retrieve relevant documents.
    """

    chunks = retrieve_relevant_chunks(question, store, top_k=3)

    context_parts = []

    for chunk in chunks:
        part = f"[Source: {chunk.chunk_id}]\n{chunk.text}"
        context_parts.append(part)

    context = "\n\n".join(context_parts)

    return context