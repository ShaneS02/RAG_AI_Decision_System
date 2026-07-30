import pytest
from Project.rag.utils.custom_exceptions import UnsupportedFileTypeError
from pathlib import Path
from unittest.mock import patch
from Project.rag.ingestion.dispatcher import (
    extract, 
    is_url,  
    retrieve_document_props, 
    detect_file_type
)

#==================================================
# tests for file type detection and URL detection
#==================================================
@pytest.mark.parametrize(
    "value, expected",
    [
        ("https://example.com", True),
        ("http://example.com", True),
        ("ftp://example.com", False),
        ("example.com", False),
        ("sample.pdf", False),
        ("C:/Users/Test/file.pdf", False),
        ("", False),
    ]
)
def test_is_url(value, expected):
    assert is_url(value) is expected



@pytest.mark.parametrize(
    "filename, expected",
    [
        ("file.pdf", "pdf"),
        ("file.PDF", "pdf"),
        ("file.docx", "docx"),
        ("file.DOCX", "docx"),
    ]
)
def test_detect_file_type(filename, expected):
    assert detect_file_type(filename) == expected


def test_detect_file_type_invalid():
    with pytest.raises(UnsupportedFileTypeError):
        detect_file_type("notes.txt")

# tests for retrieve_document_props function
docx_folder = Path("Tests/ingestion_tests/files/docx")
docx_files = list(docx_folder.glob("*.docx")) # Get all DOCX files in the folder

@pytest.mark.skipif(len(docx_files) == 0, reason="No DOCX files.")
@pytest.mark.parametrize("docx_path", docx_files)
def test_retrieve_document_props(docx_path):

    file_name, author = retrieve_document_props(docx_path)

    assert file_name == Path(docx_path).name
    assert isinstance(author, str)
    assert author.strip() != ""


#==========================
# Mock Tests for Dispatcher
#==========================


@patch("Project.rag.ingestion.dispatcher.extract_pdf_text")
def test_extract_dispatches_pdf(mock_pdf):

    mock_pdf.return_value = "PDF TEXT"

    result = extract("sample.pdf")

    mock_pdf.assert_called_once_with("sample.pdf")

    assert result["text"] == "PDF TEXT"
    assert result["metadata"]["source_type"] == "pdf"


@patch("Project.rag.ingestion.dispatcher.retrieve_document_props")
@patch("Project.rag.ingestion.dispatcher.extract_docx_text")
def test_extract_dispatches_docx(mock_docx, mock_props):

    mock_docx.return_value = "DOCX TEXT"
    mock_props.return_value = ("sample.docx", "John Smith")

    result = extract("sample.docx")

    mock_docx.assert_called_once_with("sample.docx")
    mock_props.assert_called_once_with("sample.docx")

    assert result["text"] == "DOCX TEXT"
    assert result["metadata"]["author"] == "John Smith"


@patch("Project.rag.ingestion.dispatcher.extract_html_text")
def test_extract_dispatches_html(mock_html):

    url = "https://example.com"

    mock_html.return_value = "HTML TEXT"

    result = extract(url)

    mock_html.assert_called_once_with(url)

    assert result["text"] == "HTML TEXT"
    assert result["metadata"]["source_type"] == "html"
    assert result["metadata"]["author"] == "example.com"


#============================
# Exception Handling Tests
#===========================

@patch("Project.rag.ingestion.dispatcher.extract_pdf_text")
def test_pdf_extraction_exception(mock_pdf):

    mock_pdf.side_effect = RuntimeError("Failed")

    with pytest.raises(RuntimeError):
        extract("sample.pdf")

@patch("Project.rag.ingestion.dispatcher.extract_docx_text")
def test_docx_extraction_exception(mock_docx):

    mock_docx.side_effect = RuntimeError("Failed")

    with pytest.raises(RuntimeError):
        extract("sample.docx")


@patch("Project.rag.ingestion.dispatcher.extract_html_text")
def test_html_extraction_exception(mock_html):

    mock_html.side_effect = RuntimeError("Failed")

    with pytest.raises(RuntimeError):
        extract("https://example.com")

