from typing import List
from Project import StructuredResponse

import json
import re

# =========================
# Prompt Template
# =========================

SYSTEM_PROMPT = """
You are an analytical decision-support assistant.

Your job is to analyze documents using only the information provided by the user.

Rules:
- Do not use external knowledge.
- Do not invent facts.
- Always return valid JSON only.

"""

STRUCTURED_PROMPT = """
Analyze the provided document context and answer the user's request.

User Request:
{query}

Instructions:
- Use ONLY the provided context to answer.
- Identify information that is directly stated or reasonably implied by the context.
- Do not make claims that cannot be supported by the context.
- Every factual claim must include citations using the Source IDs provided in the context.
- If a field cannot be determined from the context, use "Not found in provided sources" for that field.
- If no relevant information exists in the context, return a report indicating that no information was found.
- Output ONLY valid JSON. Do not include explanations, markdown, or text outside the JSON object.

Return a JSON object matching this structure:
{{
  "summary": "<brief summary of the document relevant to the user request>",
  "risks": [
    {{
      "description": "<identified risk>",
      "severity": "LOW | MEDIUM | HIGH",
      "rationale": "<explanation of why this is a risk based only on the context>",
      "citations": [
        "<Source>"
      ]
    }}
  ],
  "confidence_score": <number between 0 and 1>,
  "confidence_reasoning": "<reason for the confidence score based on the amount and quality of supporting information>"
}}

Context:
{context}

JSON Response:
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
            f"[Source: {chunk['citation']}]\nContent: {clean_text}"
        )

    return "\n\n".join(formatted_chunks)



def extract_json(output: str) -> dict:
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in output:\n{output}")

    print(f"JSON matched: {match.group()}")
    return match.group()

# =========================
# Structured Generation
# =========================


#Runs structured generation and returns a validated StructuredResponse. Raises if output is malformed or unsupported.
def generate_structured_response(chunks: List[dict], llm, question: str) -> StructuredResponse:
    print("Generating structured response:\n")
    context = _format_context(chunks)


    user_prompt = STRUCTURED_PROMPT.format(query=question, context=context)
    
    print("Formatted user prompt for LLM:\n")
    print(user_prompt)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    print("Formatted prompt for LLM:\n")
    prompt = llm.format_prompt_template(messages)

    # ---- CALLING LLM ---- 
    print("Calling LLM:\n")
    raw_output = llm.generate(prompt) # call the llm to generate output
    raw_output = raw_output.strip()

    print("===================Raw output from LLM ===================\n")
    print(f"Raw output from LLM:\n{raw_output}")
    print("\n=================== End of raw output ===================\n")
    

    #--- EXTRACTING JSON ----
    print("Extracting JSON:\n")
    json_str = extract_json(raw_output)
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