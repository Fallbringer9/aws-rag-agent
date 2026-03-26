from retrieval.search import retrieve_relevant_chunks
from llm.bedrock_client import generate_text_response


def build_context(chunks):
    context_parts = []

    for chunk in chunks:
        part = f"[Source: {chunk.chunk_id}]\n{chunk.text}"
        context_parts.append(part)

    return "\n\n".join(context_parts)


def build_prompt(question: str, context: str) -> str:
    return f"""
You are an AI assistant specialized in answering questions using provided context.

STRICT RULES:
- Only use the information from the context
- Do NOT use prior knowledge
- If the answer is not in the context, say:
"I don't know based on the provided information."

FORMAT:
- Give a clear and concise answer
- Then list the sources used

Context:
{context}

Question:
{question}

Answer:
""".strip()


def answer_question(question: str, store):
    chunks = retrieve_relevant_chunks(question, store, top_k=3)

    context = build_context(chunks)
    prompt = build_prompt(question, context)

    response = generate_text_response(prompt)

    return response