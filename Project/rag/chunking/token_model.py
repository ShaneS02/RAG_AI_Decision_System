from pydantic import BaseModel, Field
from typing import Callable


class TokenManager(BaseModel):
    target_tokens: int = Field(
        default=500, # Desired number of tokens per chunk
        gt=0,
        description="Chunk length in tokens"
    )

    max_tokens: int = Field(
        default=800, # Maximum allowed tokens per chunk
        gt=0,
        description="Maximum chunk length in tokens"
    )

    min_tokens: int = Field(
        default=100, # Minimum number of tokens required to form a chunk
        gt=0,
        description="Minimum chunk length in tokens"
    )

    overlap_tokens: int = Field(
        default=50, # Number of overlapping tokens between chunks
        gt=-1,
        description="Overlap length in tokens"
    )

    tokenizer : Callable

    def tokenize(self, text: str):
        return self.tokenizer(text)["input_ids"]

    def decode(self, token_ids) -> str:
        return self.tokenizer.decode(token_ids)