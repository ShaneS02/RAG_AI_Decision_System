import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1' # Disable symlink warnings for Hugging Face Hub

from Project.embeddings import EmbeddingService
import pytest
import numpy as np

@pytest.fixture(scope="module")
def embedder():
    return EmbeddingService()

def test_embedding_shape(embedder):
    embedding = embedder.embed_text("Hello world")

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert all(isinstance(x, float) for x in embedding)

#tests that embeddings are deterministic and will produce same output for same input
def test_embeddings_are_deterministic(embedder):
    e1 = embedder.embed_text("Same text")
    e2 = embedder.embed_text("Same text")

    assert e1 == e2

#tests that batch embedding matches single embeddings
def test_batch_consistency(embedder):
    texts = ["Hello", "World"]
    single_embeddings = [embedder.embed_text(t) for t in texts]
    batch_embeddings = embedder.embed_batch(texts)
    for e_single, e_batch in zip(single_embeddings, batch_embeddings):
        assert np.allclose(e_single, e_batch, atol=1e-6)

#tests that similar texts have higher similarity than dissimilar texts
def test_similarity_sanity(embedder):
    text1 = "Reset my password"
    text2 = "I forgot my login credentials"
    text3 = "The sky is blue"

    v1 = np.array(embedder.embed_text(text1))
    v2 = np.array(embedder.embed_text(text2))
    v3 = np.array(embedder.embed_text(text3))

    # Cosine similarity function
    def cos_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    assert cos_sim(v1, v2) > cos_sim(v1, v3)

#tests that embeddings are normalized and are compatible with cosine similarity
def test_normalization(embedder):
    text = "Normalization check"
    embedding = np.array(embedder.embed_text(text))

    # L2 norm should be ~1 if normalized
    norm = np.linalg.norm(embedding)
    assert np.isclose(norm, 1.0, atol=1e-5)

#tests behavior with edge case inputs
def test_edge_cases(embedder):
    texts = ["", "😀🚀✨", "a"*5000]
    for t in texts:
        e = embedder.embed_text(t)
        assert len(e) == 384
        assert all(isinstance(x, float) for x in e)