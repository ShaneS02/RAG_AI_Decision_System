#tests to ensure cleaning functions are working as expected and unnecessary text is being removed

import pytest
import re

from pathlib import Path
from Project.dispatcher import extract
from Project.text_preprocessing import clean_extracted_text


# tests folders
pdf_folder = Path("Tests/ingestion_tests/files/pdfs")
docx_folder = Path("Tests/ingestion_tests/files/docx")
html_folder = Path("Tests/ingestion_tests/files/html")

pdf_files = list(pdf_folder.glob("*.pdf")) # Get all PDF files in the folder
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder
html_urls = []
for f in html_folder.glob("*.txt"):
    # read each line in the txt file and strip whitespace
    html_urls.extend([line.strip() for line in f.read_text().splitlines() if line.strip()])

#Combine into one list
files = pdf_files + docx_files + html_urls

# Skip tests if no files found
pytestmark = pytest.mark.skipif(len(files) == 0, reason="No files found for testing.")

# --- Fixture ---
@pytest.fixture(params=files)
def extracted_text(request):
    #Fixture that yields (file_path, raw_text) for each file.
    #Extraction happens once per file.
    file = request.param
    raw_text = extract(file)["text"]
    return file, clean_extracted_text(raw_text)

# --- Test functions ---

def test_remove_page_numbers(extracted_text):
    file, cleaned = extracted_text
    assert not any(f"Page {i} of" in cleaned for i in range(1, 1000)), f"Page numbers found in {file.name}"

def test_remove_headers(extracted_text):
    file, cleaned = extracted_text
    assert "Header:" not in cleaned, f"Header found in {file.name}"

def test_remove_footers(extracted_text):
    file, cleaned = extracted_text
    assert "Footer:" not in cleaned, f"Footer found in {file.name}"

def test_remove_timestamps(extracted_text):
    file, cleaned = extracted_text
    timestamp_pattern = r'\d{1,2}/\d{1,2}/\d{2,4} \d{1,2}:\d{2} (AM|PM)?'
    assert not re.search(timestamp_pattern, cleaned), f"Timestamps found in {file.name}"

def test_remove_file_paths(extracted_text):
    file, cleaned = extracted_text
    file_path_pattern = r'([a-zA-Z]:)?(\\[a-zA-Z0-9_.-]+)+\\?'
    assert not re.search(file_path_pattern, cleaned), f"File paths found in {file.name}"

def test_remove_tracking_ids(extracted_text):
    file, cleaned = extracted_text 
    tracking_pattern = r'Tracking ID: \w+'
    assert not re.search(tracking_pattern, cleaned), f"Tracking IDs found in {file.name}"

def test_no_extra_newlines(extracted_text):
    file, cleaned = extracted_text
    assert "\n\n" not in cleaned, f"double newlines found in {file.name}"

def test_no_double_spaces(extracted_text):
    file, cleaned = extracted_text 
    assert "  " not in cleaned, f"Double spaces found in {file.name}"

def test_cleaned_text_not_empty(extracted_text):
    file, cleaned = extracted_text
    assert cleaned.strip() != "", f"Cleaned text is empty for {file.name}"