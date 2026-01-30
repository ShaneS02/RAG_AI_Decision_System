# Tests for chunking functionality

from Project.chunking import chunk_text  # Assuming the chunking function is in chunking_module.py

def simple_tokenizer(text: str):
    return text.split()

def test_empty_input():
    chunks = chunk_text("", simple_tokenizer)
    assert chunks == []

def test_whitespace_input():
    chunks = chunk_text("   \n\n  ", simple_tokenizer)
    assert chunks == []


def test_chunk_size_limits():
    text = "\n".join(["word " * 100] * 10)  # 1000 tokens

    chunks = chunk_text(
        text,
        simple_tokenizer,
        target_tokens=200,
        max_tokens=300
    )

    for chunk in chunks:
        assert chunk["token_count"] <= 300

def test_paragraph_preservation():
    text = "para1 words\npara2 more words\npara3 even more words"

    chunks = chunk_text(
        text,
        simple_tokenizer,
        target_tokens=50
    )

    combined = " ".join(c["text"] for c in chunks)

    assert "para1 words" in combined
    assert "para2 more words" in combined
    assert "para3 even more words" in combined

def test_oversized_paragraph_is_split():
    text = "word " * 1000  # one huge paragraph

    chunks = chunk_text(
        text,
        simple_tokenizer,
        target_tokens=200,
        max_tokens=300,
        overlap_tokens=20
    )

    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk["token_count"] <= 300

def test_overlap_between_chunks():
    text = " ".join(f"word{i}" for i in range(500))

    chunks = chunk_text(
        text,
        simple_tokenizer,
        target_tokens=100,
        overlap_tokens=10
    )

    first = chunks[0]["text"].split()
    second = chunks[1]["text"].split()

    overlap = set(first[-10:]) & set(second[:10])
    assert len(overlap) > 0

def test_small_chunks_are_merged():
    text = "word " * 50 + "\n" + "word " * 5  # second paragraph tiny

    chunks = chunk_text(
        text,
        simple_tokenizer,
        target_tokens=100,
        min_tokens=20
    )

    assert len(chunks) == 1

#tests that the same input always produces the same chunks
def test_chunking_is_deterministic():
    text = "word " * 300

    chunks1 = chunk_text(text, simple_tokenizer)
    chunks2 = chunk_text(text, simple_tokenizer)

    assert chunks1 == chunks2