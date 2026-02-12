from typing import List
from Project import generate_structured_response
from Project import StructuredResponse

import logging

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm

    async def analyze(self, query: str) -> StructuredResponse:
        logger.info("Analyze request received", extra={"text_length": len(query)})

        # Retrieve chunks
        chunks, _ = self.vector_store.search(
            query=query,
            top_k=5
        )

        if not chunks:
            raise ValueError("No relevant context retrieved")

        # Retrieve the Structured response from llm answer
        structured_response = generate_structured_response(
            chunks=chunks,
            llm=self.llm
        )

        return structured_response