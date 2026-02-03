from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional

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