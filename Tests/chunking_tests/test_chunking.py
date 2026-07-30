# Tests for chunking functionality

from Project import chunk_text, TokenManager

class SimpleTokenizer:
    def __call__(self, text: str):
        return {
            "input_ids": text.split()
        }

    def decode(self, token_ids):
        return " ".join(token_ids)



def test_empty_input():
    chunks = chunk_text("", TokenManager(tokenizer=SimpleTokenizer()))
    assert chunks == []

def test_whitespace_input():
    chunks = chunk_text("   \n\n  ", TokenManager(tokenizer=SimpleTokenizer()))
    assert chunks == []


def test_chunk_size_limits():
    text = "\n".join(["word " * 100] * 10)  # 1000 tokens

    chunks = chunk_text(
        text,
        TokenManager(tokenizer=SimpleTokenizer(), target_tokens=200, max_tokens=300)
    )

    for chunk in chunks:
        assert chunk["token_count"] <= 300

def test_paragraph_preservation():
    text = "para1 words\npara2 more words\npara3 even more words"

    chunks = chunk_text(
        text,
        TokenManager(tokenizer=SimpleTokenizer(), target_tokens=50)
    )

    combined = " ".join(c["text"] for c in chunks)

    assert "para1 words" in combined
    assert "para2 more words" in combined
    assert "para3 even more words" in combined

def test_oversized_paragraph_is_split():
    text = "word " * 1000  # one huge paragraph

    chunks = chunk_text(
        text,
        TokenManager(tokenizer=SimpleTokenizer(), target_tokens=200, max_tokens=300, overlap_tokens=20)
    )

    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk["token_count"] <= 300

def test_overlap_between_chunks():
    text = " ".join(f"word{i}" for i in range(500))

    chunks = chunk_text(
        text,
        TokenManager(tokenizer=SimpleTokenizer(), target_tokens=100, max_tokens=150, overlap_tokens=10)
    )

    first = chunks[0]["text"].split()
    second = chunks[1]["text"].split()

    overlap = set(first[-10:]) & set(second[:10])
    assert len(overlap) > 0

def test_small_chunks_are_merged():
    text = "word " * 50 + "\n" + "word " * 5  # second paragraph tiny

    chunks = chunk_text(
        text,
        TokenManager(tokenizer=SimpleTokenizer(), target_tokens=100, min_tokens=20)
    )

    assert len(chunks) == 1

#tests that the same input always produces the same chunks
def test_chunking_is_deterministic():
    text = "word " * 300

    chunks1 = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer()))
    chunks2 = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer()))

    assert chunks1 == chunks2

def test_exactly_target_tokens():
    text = "word " * 200

    chunks = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer(), target_tokens=200,max_tokens=300))

    assert len(chunks) == 1
    assert chunks[0]["token_count"] == 200

def test_exactly_max_tokens():
    text = "word " * 300

    chunks = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer(),target_tokens=300, max_tokens=300))

    assert len(chunks) == 1
    assert chunks[0]["token_count"] == 300


def test_exactly_min_tokens_not_merged():
    text = ("word " * 20).strip() + "\n" + ("word " * 20).strip()

    chunks = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer(), target_tokens=25, max_tokens=100, min_tokens=20))

    assert len(chunks) == 2

def test_no_overlap_between_chunks():
    text = " ".join(f"word{i}" for i in range(500))

    chunks = chunk_text(text,  TokenManager(tokenizer=SimpleTokenizer(), target_tokens=100, max_tokens=150, overlap_tokens=0))

    first = chunks[0]["text"].split()
    second = chunks[1]["text"].split()

    assert set(first[-10:]).isdisjoint(second[:10]) #checks if tokens intersect

def test_small_chunk_not_merged_when_exceeding_max():
    text = (("word " * 290).strip() + "\n" + ("tiny " * 20).strip())

    chunks = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer(),target_tokens=300, max_tokens=300, min_tokens=50))

    assert len(chunks) == 2

def test_large_chunks_not_merged():
    text = (("word " * 100).strip() + "\n" + ("word " * 100).strip())

    chunks = chunk_text(text, TokenManager(tokenizer=SimpleTokenizer(), target_tokens=100, max_tokens=300, min_tokens=50))

    assert len(chunks) == 2