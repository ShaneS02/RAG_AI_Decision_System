#tests to ensure cleaning functions are working as expected and unnecessary text is being removed

import pytest

from pathlib import Path
from Project.text_preprocessing import (
    extract_pdf_text, 
    extract_docx_text, 
    extract_html_text,
    clean_extracted_text
)


#folders containing test files
pdf_folder = Path("Tests/files/pdfs")
docx_folder = Path("Tests/files/docx")
html_folder = Path("Tests/files/html")

pdf_files = list(pdf_folder.glob("*.pdf")) # Get all PDF files in the folder
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder
html_files = list(html_folder.glob("*.txt")) # Get all files with url links


@pytest.fixture(scope="module")
def raw_pdf_text():    
    return {f.name: extract_pdf_text(f) for f in pdf_folder.glob("*.pdf")}

@pytest.fixture(scope="module")
def raw_docx_text():
    return {f.name: extract_docx_text(f) for f in docx_folder.glob("*.docx")}

@pytest.fixture(scope="module")
def raw_html_text():
    texts = {}
    for html_path in html_folder.glob("*.pdf"):
        with open(html_path, 'r', encoding='utf-8') as f:
            url = f.read().strip()

        texts[url] = extract_html_text(url)
    return texts

@pytest.mark.skipif(len(pdf_files) == 0, reason="No PDF files found for testing.")
@pytest.mark.parametrize("pdf_file", pdf_files) #run test with all pdf files found
def test_remove_page_numbers(raw_pdf_text, pdf_file):
    raw = raw_pdf_text[pdf_file.name]
    cleaned = clean_extracted_text(raw)
    
    
    assert "Header:" not in cleaned
    assert cleaned.strip() != ""