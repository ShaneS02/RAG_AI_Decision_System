#tests to standardize information from various sources into a common format

import pytest
import uuid

from Project.documents_ingestion import ingestion
from pathlib import Path
from datetime import datetime

# tests folders
pdf_folder = Path("Tests/files/pdfs")
docx_folder = Path("Tests/files/docx")
html_folder = Path("Tests/files/html")

pdf_files = list(pdf_folder.glob("*.pdf")) # Get all PDF files in the folder
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder

html_urls = []
for f in html_folder.glob("*.txt"):
    # read each line in the txt file and strip whitespace
    html_urls.extend([line.strip() for line in f.read_text().splitlines() if line.strip()])

# Combine into one list
files = pdf_files + docx_files + html_urls

# Skip tests if no files found
pytestmark = pytest.mark.skipif(len(files) == 0, reason="No files found for testing.")

@pytest.fixture(params=files)
def extracted_text(request):
    file = request.param
    normalized_dictionary = ingestion(file)
    return normalized_dictionary

# --- Test functions ---
def test_normalize_document_schema(extracted_text):
    result = extracted_text

    assert isinstance(result, dict)
    assert set(result.keys()) == {
        "id",
        "text",
        "source",
        "metadata",
        "ingested_at"
    }
    assert isinstance(result["metadata"], dict)

def test_normalize_document_insertions(extracted_text):
    result = extracted_text
    assert result["text"] != ""
    assert result["source"] == "html" or "pdf" or "docx"


def test_normalize_document_generates_uuid(extracted_text):
    result = extracted_text
    uuid.UUID(result["id"]) 



def test_normalize_document_ingested_at_isoformat(extracted_text):
    result = extracted_text

    parsed = datetime.fromisoformat(result["ingested_at"])
    assert parsed.tzinfo is not None
