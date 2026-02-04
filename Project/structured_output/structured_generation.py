from typing import List
from Project.utils.validators import StructuredResponse

import json

# =========================
# Prompt Template
# =========================


STRUCTURED_PROMPT = """
You are an analytical decision-support system.

Using ONLY the provided context, generate a response that strictly follows the JSON schema below.

Rules:
- Do not use external knowledge
- Do not speculate
- If information is missing, say "Not found in provided sources"
- Every factual claim must be supported by citations
- Citations MUST match the citation IDs in the context
- Output ONLY valid JSON
- Do NOT include explanations outside the JSON

JSON Schema:
{{
  "summary": string,
  "risks": [
    {{
      "description": string,
      "severity": "LOW" | "MEDIUM" | "HIGH",
      "rationale": string,
      "citations": [string]
    }}
  ],
  "confidence_score": number,
  "confidence_reasoning": string
}}

Context:
{context}
"""


# =========================
# 3. Context Formatting
# =========================

def format_context(chunks: List[dict]) -> str:    
    formatted_chunks = []

    for chunk in chunks:
        formatted_chunks.append(
            f"[{chunk['citation']}]\n{chunk['text']}"
        )

    return "\n\n".join(formatted_chunks)

# =========================
# Structured Generation
# =========================


#Runs structured generation and returns a validated StructuredResponse. Raises if output is malformed or unsupported.
def generate_structured_response(chunks: List[dict], llm) -> StructuredResponse:
    context = format_context(chunks)
    prompt = STRUCTURED_PROMPT.format(context=context)

    # ---- CALLING LLM ---- 
    raw_output = llm.generate(prompt) # call the llm to generate output

    # ---- PARSING JSON ---- 
    try:
      parsed = json.loads(raw_output) #converts json formatted string to python object 
    except json.JSONDecodeError as e:
      raise ValueError(f"LLM did not return valid JSON: {e}\nOutput:\n{raw_output}")

    # ---- SCHEMA VALIDATION ----
    try:
      validated = StructuredResponse.model_validate(parsed)
    except Exception as e:
      raise ValueError(f"Structured response validation failed: {e}")

    return validated