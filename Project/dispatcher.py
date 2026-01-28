from docx import Document
from urllib.parse import urlparse  # For URL parsing
from pathlib import Path
from .text_preprocessing import extract_html_text, extract_pdf_text, extract_docx_text
from .custom_exceptions import UnsupportedFileTypeError

SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "docx",
}

#function to retrieve document properties like title and author
def retrieve_document_props(file_path):
    props = Document(file_path).core_properties # Access core properties  
    return Path(file_path).name, props.author or "unknown" 


#function to check if a string is a URL
def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https")

#function to detect file type based on extension
def detect_file_type(file_path):
    ext = Path(file_path).suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")
    
    return SUPPORTED_EXTENSIONS[ext]

#function to extract text and metadata based on file type
def extract(file_path):
    #string object for file path is created to account for both URL and local file paths
    if is_url(str(file_path)):
        file_type = "html"
        file_name = file_path
        author = urlparse(file_path).netloc or "unknown" #unknown is for safety
        raw_text = extract_html_text(file_path)
    else:
        file_type = detect_file_type(file_path)

        if file_type == "pdf":
            raw_text = extract_pdf_text(file_path)
            # PDFs are not Office packages; don't call python-docx on them.
            file_name = Path(file_path).name
            author = "unknown"
        elif file_type == "docx":
            raw_text = extract_docx_text(file_path)
            file_name, author = retrieve_document_props(file_path)
        else:
            raise UnsupportedFileTypeError(file_type)  # Just a safety check
    
    
    #extracted text and metadata dictionary
    return {
        "text": raw_text,        # string returned from PyPDF2 / python-docx / BeautifulSoup
        "metadata": {
            "source_type": file_type,
            "file_name": file_name,
            "author": author
        }
    }