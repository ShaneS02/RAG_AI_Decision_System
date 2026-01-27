#custom exception class for unsupported file types
class UnsupportedFileTypeError(Exception):
    """Raised when an unsupported file type is passed to ingestion."""
    pass
