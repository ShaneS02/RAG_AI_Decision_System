from .text_preprocessing import clean_extracted_text, normalize_document
from .dispatcher import extract


#function to handle the complete ingestion process
def ingestion(file_path):  
    extracted = extract(file_path)     # PDF / HTML / DOCX
    cleaned_text = clean_extracted_text(extracted["text"])
    extracted["text"] = cleaned_text
    return normalize_document(extracted) 