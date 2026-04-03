from typing import List
from Project import StructuredResponse

import json
import re

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

Generate a JSON object matching the schema below, filling all fields 
with real data from the context. Do not output the schema itself.

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

Task:
Using the context above, fill the JSON schema with actual information. 
If a value is missing in the context, use "Not found in provided sources" or 0.0 as appropriate.
Output ONLY the JSON.

Below is an example. Note, This is just an example of formatting, fill all fields with actual information.
Example output:
{{
  "summary": "Not found in provided sources",
  "risks": [],
  "confidence_score": 0.0,
  "confidence_reasoning": "No relevant information found"
}}
"""


# =========================
# 3. Context Formatting
# =========================

def _normalize_text(text: str) -> str:
    # Replace [SEP] with newline
    text = text.replace("[SEP]", "\n")
    
    # Replace repeated underscores with newline
    text = re.sub(r'_+ ?', '\n', text)
    
    # Collapse multiple blank lines into one
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()

def _format_context(chunks: List[dict]) -> str:    
    formatted_chunks = []

    for chunk in chunks:
        clean_text = _normalize_text(chunk['text'])
        formatted_chunks.append(
            f"[{chunk['citation']}]\n{clean_text}"
        )

    return "\n\n".join(formatted_chunks)



def extract_json(text: str) -> str:
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    else:
        raise ValueError(f"No JSON object found in LLM output:\n{text}")

# =========================
# Structured Generation
# =========================


#Runs structured generation and returns a validated StructuredResponse. Raises if output is malformed or unsupported.
def generate_structured_response(chunks: List[dict], llm) -> StructuredResponse:
    context = _format_context(chunks)
    prompt = STRUCTURED_PROMPT.format(context=context)

    # ---- CALLING LLM ---- 
    raw_output = llm.generate(prompt) # call the llm to generate output

    #--- EXTRACTING JSON ----
    json_str = extract_json(raw_output)
    print(f"Extracted JSON string from LLM output:\n{json_str}")
    print(f"End of extracted JSON string")

    # ---- PARSING JSON ---- 
    try:
      parsed = json.loads(json_str) #converts json formatted string to python object 
    except json.JSONDecodeError as e:
      raise ValueError(f"LLM did not return valid JSON: {e}\nOutput:\n{raw_output}")

    # ---- SCHEMA VALIDATION ----
    try:
      validated = StructuredResponse.model_validate(parsed)
    except Exception as e:
      raise ValueError(f"Structured response validation failed: {e}")

    return validated