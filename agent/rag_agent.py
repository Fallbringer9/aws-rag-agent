from strands import Agent
from strands.tools import tool

from tools.retrieval_tool import retrieval_tool


def create_rag_agent(store):
    @tool
    def retrieval_tool_for_agent(query: str) -> str:
        """
        Retrieve relevant context from the indexed documents for a user question.
        """
        return retrieval_tool(query, store)

    system_prompt = """
You are a helpful RAG assistant.

You have access to a retrieval tool that returns relevant document context.

Rules:
- Always use the retrieval_tool_for_agent tool when the user asks about the indexed documents.
- Use ONLY the information returned by the retrieval tool.
- Do NOT invent facts.
- If the retrieved context does not contain the answer, say:
  "I don't know based on the provided information."
- Be concise and accurate.
- At the end of your answer, cite the relevant sources when available.
""".strip()

    agent = Agent(
        system_prompt=system_prompt,
        tools=[retrieval_tool_for_agent],
    )

    return agent