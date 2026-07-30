#test the dispatcher ( the extract function ) to ensure all file types are being routed correctly

import pytest
from pathlib import Path
from Project.rag.ingestion.dispatcher import extract
from Project.rag.utils.custom_exceptions import UnsupportedFileTypeError


# tests folders
pdf_folder = Path("Tests/ingestion_tests/files/pdfs")
docx_folder = Path("Tests/ingestion_tests/files/docx")
html_folder = Path("Tests/ingestion_tests/files/html")

pdf_files = list(pdf_folder.glob("*.pdf")) # Get all PDF files in the folder
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder
html_files = list(html_folder.glob("*.txt")) # Get all files with url links

urls = []
for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        urls.append(f.read().strip())



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
@pytest.mark.parametrize("url", urls) #run test with all html files found
def test_extract_html_dispatch(url):
    result = extract(url)

    assert isinstance(result, dict)
    assert "text" in result
    assert "metadata" in result

    assert result["metadata"]["source_type"] == "html"
    assert result["metadata"]["file_name"] == url
    assert result["metadata"]["author"] != ""


# test that an unsupported file type raises the correct exception
def test_extract_unsupported_file():

    with pytest.raises(UnsupportedFileTypeError):
        extract("fake_file.txt")



# test that the extract function returns the expected structure for supported file types
@pytest.mark.parametrize(
    "path",
    [
        pdf_files[0],
        docx_files[0],
        urls[0],
    ]
)
def test_extract_returns_expected_structure(path):

    result = extract(path)

    assert isinstance(result, dict)

    assert set(result.keys()) == {
        "text",
        "metadata"
    }

    assert isinstance(result["text"], str)

    assert isinstance(result["metadata"], dict)

    assert set(result["metadata"].keys()) == {
        "source_type",
        "file_name",
        "author"
    }