#test the dispatcher ( the extract function ) to ensure all file types are being routed correctly

import pytest
from pathlib import Path
from Project.dispatcher import extract


# tests folders
pdf_folder = Path("files/pdfs")
docx_folder = Path("files/docx")
html_folder = Path("files/html")

pdf_files = list(pdf_folder.glob("*.pdf")) # Get all PDF files in the folder
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder
html_files = list(html_folder.glob("*.txt")) # Get all files with url links

#skip test if no pdf files found
@pytest.mark.skipif(len(pdf_files) == 0, reason="No PDF files found for testing.")
@pytest.mark.parametrize("pdf_path", pdf_files) #run test with all pdf files found
def test_extract_pdf_dispatch(pdf_path):
    result = extract(pdf_path)

    assert isinstance(result, dict)
    assert "text" in result
    assert "metadata" in result

    assert result["metadata"]["source_type"] == "pdf"
    assert result["metadata"]["file_name"] == Path(pdf_path).name
    assert result["metadata"]["author"] == "unknown"


#skip test if no docx files found
@pytest.mark.skipif(len(docx_files) == 0, reason="No PDF files found for testing.")
@pytest.mark.parametrize("docx_path", docx_files) #run test with all pdf files found
def test_extract_docx_dispatch(docx_path):
    result = extract(docx_path)

    assert isinstance(result, dict)
    assert "text" in result
    assert "metadata" in result

    assert result["metadata"]["source_type"] == "docx"
    assert result["metadata"]["file_name"] == Path(docx_path).name
    assert result["metadata"]["author"] != ""


#skip test if no html files found
@pytest.mark.skipif(len(html_files) == 0, reason="No HTML URL files found for testing.")
@pytest.mark.parametrize("html_path", html_files) #run test with all html files found
def test_extract_html_dispatch(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        url = f.read().strip()

    result = extract(url)

    assert isinstance(result, dict)
    assert "text" in result
    assert "metadata" in result

    assert result["metadata"]["source_type"] == "html"
    assert result["metadata"]["file_name"] == url
    assert result["metadata"]["author"] != ""