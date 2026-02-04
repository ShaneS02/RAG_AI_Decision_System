from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Literal

# ==================================
# Vector Database Schema for Chunks
# ==================================


class Chunk(BaseModel):
    document_id: str
    chunk_id: str
    text: str
    file_name: str
    source: str
    metadata: Dict = {}
    created_at: datetime 
    citation: str

    @field_validator("document_id", "chunk_id", "text", "file_name", "source", "citation")
    def not_empty(value, info):
        if not value or not str(value).strip():
            raise ValueError(f"{info.field.name} cannot be empty")
        


# ===============================
# Structured Query Output Schema
# ===============================

class RiskItem(BaseModel):
    description: str
    severity: Literal["LOW", "MEDIUM", "HIGH"]
    rationale: str
    citations: List[str]

class StructuredResponse(BaseModel):
    summary: str
    risks: list[RiskItem]
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_reasoning: str