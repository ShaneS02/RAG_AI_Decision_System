#tests if the extractors are working properly and text is being extracted as expected
import pytest
from Project.text_preprocessing import extract_html_text, extract_pdf_text, extract_docx_text
from pathlib import Path

#folders containing test files
pdf_folder = Path("Tests/ingestion_tests/files/pdfs")
docx_folder = Path("Tests/ingestion_tests/files/docx")
html_folder = Path("Tests/ingestion_tests/files/html")

pdf_files = list(pdf_folder.glob("*.pdf")) # Get all PDF files in the folder
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder
html_files = list(html_folder.glob("*.txt")) # Get all files with url links

#skip test if no pdf files found
@pytest.mark.skipif(len(pdf_files) == 0, reason="No PDF files found for testing.")
@pytest.mark.parametrize("pdf_path", pdf_files) #run test with all pdf files found
def test_extract_pdf_text(pdf_path): 
    extracted_text = extract_pdf_text(pdf_path)
    assert isinstance(extracted_text, str)
    assert extracted_text != "\n"
    assert len(extracted_text.strip()) > 0  # Ensure some text was extracted

#skip test if no docx files found
@pytest.mark.skipif(len(docx_files) == 0, reason="No DOCX files found for testing.")
@pytest.mark.parametrize("docx_path", docx_files) #run test with all docx files found
def test_extract_docx_text(docx_path): 
    extracted_text = extract_docx_text(docx_path)
    assert isinstance(extracted_text, str)
    assert extracted_text != "\n"
    assert len(extracted_text.strip()) > 0  # Ensure some text was extracted

#skip test if no html files found
@pytest.mark.skipif(len(html_files) == 0, reason="No HTML URL files found for testing.")
@pytest.mark.parametrize("html_path", html_files) #run test with all html files found
def test_extract_html_text(html_path): 
    with open(html_path, 'r', encoding='utf-8') as f:
        url = f.read().strip()
    
    extracted_text = extract_html_text(url)
    assert isinstance(extracted_text, str)
    assert len(extracted_text.strip()) > 0  # Ensure some text was extracted