# RAG_AI_Decision_System

## Document Ingestion Process

The document ingestion pipeline is a three-stage workflow that extracts, cleans, and normalizes text from multiple document formats to prepare them for downstream processing (chunking and embedding).

### Overview

The ingestion process transforms raw documents (PDF, DOCX, HTML) into standardized, structured documents with metadata. The workflow consists of three main components working in sequence:

2. **Dispatcher** - Detects file type and extracts raw text with metadata
1. **Text Preprocessing** - Cleans and normalizes the extracted text
3. **Documents Ingestion** - Orchestrates the complete pipeline and returns structured output

### Detailed Workflow

#### Stage 1: Dispatch & Extraction (dispatcher.py)

The dispatcher module handles file type detection and raw text extraction.

**Key Functions:**

- **`detect_file_type(file_path)`** - Determines the document format based on file extension
  - Supports: `.pdf`, `.docx`, and URLs
  - Raises `UnsupportedFileTypeError` for unsupported formats

- **`is_url(value)`** - Identifies whether the input is a URL or local file path
  - Validates HTTP/HTTPS schemes for web content

- **`extract(file_path)`** - Extracts raw text and metadata based on document type
  - **PDF Files**: Extracts text from all pages using PyPDF
  - **DOCX Files**: Extracts text from paragraphs using python-docx and retrieves document properties (author, title)
  - **URLs/HTML**: Fetches HTML content and parses it with BeautifulSoup, removing scripts, styles, navigation, and footer elements

**Output Format:**
```python
{
    "text": "raw extracted text",
    "metadata": {
        "source_type": "pdf|docx|html",
        "file_name": "document name or URL",
        "author": "document author or domain"
    }
}
```

#### Stage 2: Text Cleaning & Normalization (text_preprocessing.py)

The text preprocessing module cleans and normalizes the extracted text for consistency.

**Key Functions:**

- **`clean_extracted_text(text)`** - Removes artifacts and noise from extracted text
  - Removes page number patterns (e.g., "Page 1 of 10")
  - Strips header/footer text blocks
  - Removes timestamps and date patterns
  - Eliminates file paths (Windows/Unix style)
  - Removes tracking IDs and identifiers
  - Consolidates multiple whitespace and newlines into single spaces/lines

- **`normalize_document(extracted)`** - Structures the cleaned document with metadata
  - Assigns a unique UUID identifier
  - Preserves cleaned text and source metadata
  - Adds ISO 8601 timestamp of ingestion (`ingested_at`)

**Output Format:**
```python
{
    "id": "uuid-4-identifier",
    "text": "cleaned and normalized text",
    "source": "pdf|docx|html",
    "metadata": {
        "source_type": "pdf|docx|html",
        "file_name": "...",
        "author": "..."
    },
    "ingested_at": "2026-01-29T10:30:45.123456+00:00"
}
```

#### Stage 3: Pipeline Orchestration (documents_ingestion.py)

The ingestion module coordinates the complete end-to-end workflow.

**Key Function:**

- **`ingestion(file_path)`** - Executes the full ingestion pipeline
  1. Calls `extract()` to get raw text and metadata from dispatcher
  2. Passes raw text through `clean_extracted_text()` to remove noise
  3. Updates the extracted data with cleaned text
  4. Normalizes the document with `normalize_document()` to add ID and timestamp
  5. Returns the final structured document

### Complete Flow Diagram

```
Input File (PDF/DOCX/URL)
    ↓
[Dispatcher] Extract & Detect
    ├─ detect_file_type() → identifies format
    ├─ extract() → retrieves raw text + metadata
    ↓
Raw Text + Metadata
    ↓
[Text Preprocessing] Clean & Normalize
    ├─ clean_extracted_text() → removes artifacts
    ├─ normalize_document() → adds ID + timestamp
    ↓
Structured Document
    ↓
[Chunking Phase] → Ready for downstream processing
```

### Error Handling

- **Unsupported File Types**: Raises `UnsupportedFileTypeError`
- **HTML Requests**: Handles connection errors, timeouts, and HTTP errors gracefully
- **Missing Properties**: Uses fallback values ("unknown") for missing metadata fields

### Supported Document Types

| Format | Extractor | Metadata |
|--------|-----------|----------|
| PDF | PyPDF (page-by-page extraction) | Filename, Author (unknown) |
| DOCX | python-docx (paragraph extraction) | Filename, Author, Title |
| HTML/URL | BeautifulSoup (DOM parsing) | URL, Domain as Author |

---

# Chunking Phase Explanation

I applied paragraph-aware, token-bounded chunking after text normalization. Chunks are formed by grouping cleaned paragraphs up to a target token size, with limited overlap to preserve local context. A token-based sliding window is used as a fallback for unstructured or oversized text segments