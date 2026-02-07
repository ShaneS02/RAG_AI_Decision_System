from typing import List
from Project import generate_structured_response
from Project import StructuredResponse


class RAGService:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    async def analyze(self, query: str) -> StructuredResponse:
        # Retrieve chunks
        chunks: List[dict] = self.vector_store.search(
            query=query,
            k=5
        )

        if not chunks:
            raise ValueError("No relevant context retrieved")

        # Retrieve the Structured response from llm answer
        structured_response = generate_structured_response(
            chunks=chunks,
            llm=self.llm
        )

        return structured_response