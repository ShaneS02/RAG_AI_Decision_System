from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup # HTML parsing
from datetime import datetime, timezone

import re # Regular expressions for text cleaning
import uuid 
import requests # For fetching HTML content from URLs


#function to extract text from each page in the pdf document 
#or return an empty string if nothing is returned
def extract_pdf_text(path):
    reader = PdfReader(path)    
    return "\n".join(page.extract_text() or "" for page in reader.pages)

#function to extract text from the each paragraph in the html document 
def extract_docx_text(path):
    doc = Document(path)
    return "\n".join(para.text for para in doc.paragraphs)

#function to extract text from html content
def extract_html_text(file_path):
    # Fetch HTML content from the URL and handle potential request errors
    try:
        response = requests.get(file_path, timeout=10) # Fetch HTML content from URL with 10s timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx, 5xx)
        html = response.text # Get HTML content
    except requests.exceptions.ConnectionError:
        raise Exception(f"Connection failed: Unable to reach {file_path}")
    except requests.exceptions.Timeout:
        raise Exception(f"Request timeout: {file_path} took too long to respond")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    
    # Parse HTML and extract text    
    soup = BeautifulSoup(html, 'html.parser')

    # Remove scripts, styles, nac & footer
    for element in soup(['script', 'style', 'nav', 'footer']):
        element.decompose()

    return soup.get_text(separator='\n', strip=True)

#function to clean the extracted text
# Removes things like Page numbers, Headers/footers, Timestamps, File paths, Tracking IDs
def clean_extracted_text(text):
    if not text:
        return ""
     
    cleaned_text = re.sub(r'Page \d+ of \d+', '', text)  # Remove page numbers
    cleaned_text = re.sub(r'Header:.*\n', '', cleaned_text)  # Remove headers
    cleaned_text = re.sub(r'Footer:.*\n', '', cleaned_text)  # Remove footers
    cleaned_text = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4} \d{1,2}:\d{2} (AM|PM)?', '', cleaned_text)  # Remove timestamps
    cleaned_text = re.sub(r'([a-zA-Z]:)?(\\[a-zA-Z0-9_.-]+)+\\?', '', cleaned_text)  # Remove file paths
    cleaned_text = re.sub(r'Tracking ID: \w+', '', cleaned_text)  # Remove tracking IDs
    cleaned_text = re.sub(r'\n{2,}', '\n', cleaned_text)  # Remove extra newlines
    cleaned_text = re.sub(r"\s{2,}", " ", cleaned_text)   # Remove extra spaces
    return cleaned_text.strip()

#function to normalize document with cleaned extracted text
def normalize_document(extracted):
    return { 
        "id": str(uuid.uuid4()), # Unique identifier for the document
        "text": extracted["text"].strip(), # Cleaned and normalized text content
        "source": extracted["metadata"]["source_type"], # Original source of the document
        "metadata": extracted["metadata"], # Additional metadata associated with the document
        "ingested_at": datetime.now(timezone.utc).isoformat() # Timestamp of ingestion in ISO 8601 format
    }