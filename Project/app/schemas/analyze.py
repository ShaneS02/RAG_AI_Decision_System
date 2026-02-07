from pydantic import BaseModel, Field
from typing import List

from Project import StructuredResponse




class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="User input to analyze")


# API-level alias
AnalyzeResponse = StructuredResponse