from typing import List
from Project import generate_structured_response
from Project import StructuredResponse
from Project import ingestion, chunk_text

import logging

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm
     
    async def upload(self, file):
        #extract and normalize text from document/url
        extracted_text = ingestion(file)

        #chunk and embed the extracted text
        tokenizer = self.vector_store.embedding_service.tokenizer()
        chunks = chunk_text(text=extracted_text["text"], tokenize_fn=tokenizer)
        prepared_chunks = self.vector_store.prepare_chunks(extracted_text, chunks)
        
        #Store info in the vector database
        self.vector_store.add_chunks(prepared_chunks)

        return


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