import faiss
import numpy as np

from typing import Dict, List

class VectorDatabase:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.dim = embedding_service.get_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dim) # Create a FAISS index
        self.metadata = []  # list of dicts corresponding to each vector
    
    #ensure chunks are properly formatted and consists of the required keys
    def _validate_chunk(self, chunk: Dict):
        # Required keys
        required_keys = ["document_id", "text", "source", "metadata"]
        
        # Check all keys exist
        for key in required_keys:
            if key not in chunk:
                return False
        
        # Check types
        if not isinstance(chunk["document_id"], str):
            return False
        if not isinstance(chunk["text"], str) or not chunk["text"].strip():
            return False
        if not isinstance(chunk["source"], str) and chunk["source"] is not None:
            return False
        if not isinstance(chunk["metadata"], dict):
            return False

        return True
    
    #properly format chunks
    def prepare_chunks(self, document: Dict, chunks: List):
        prepared_chunks = []

        for chunk in chunks:
            # Store chunk with metadata
            formatted = ({
                "document_id": document["id"],
                "text": chunk["text"],
                "source": document["source"],
                "metadata": document["metadata"]
            })

            #check for malformed chunks
            if not self._validate_chunk(formatted):
                raise ValueError(f"Chunk is invalid: {formatted}")
            
            prepared_chunks.append(formatted)
            
        return prepared_chunks

    # Add chunks to the FAISS index
    def add_chunks(self, chunks : List[Dict]):

        #check if chunk is properly formatted
        for chunk in chunks:
            if not self._validate_chunk(chunk):
                raise ValueError(f"Invalid chunk: {chunk}")

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_service.embed_batch(texts)
        vectors = np.array(embeddings, dtype="float32")
        self.index.add(vectors)
        self.metadata.extend(chunks)

    # Search the FAISS index for similar vectors
    def search(self, query: str, top_k: int = 5, min_similarity = 0.75):
        query_embedding = self.embedding_service.embed_text(query)
        query_vector = np.array([query_embedding], dtype="float32") # FAISS expects 2D array
        scores, indices = self.index.search(query_vector, top_k) #scores shape (1, top_k), indices shape (1, top_k) 

        results = []  
        filtered_scores = []

        #filter results below the min similarity
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or score < min_similarity:
                continue   # Not relevant

            results.append(self.metadata[idx]) 
            filtered_scores.append(score)

        if not results:
            return [], None
        
        return results, filtered_scores

    # Save and load the FAISS index and metadata 
    def save(self, index_path, metadata_path):
        faiss.write_index(self.index, index_path)
        np.save(metadata_path, np.array(self.metadata, dtype=object))

    # Load the FAISS index and metadata
    def load(self, index_path, metadata_path):
        self.index = faiss.read_index(index_path)
        self.metadata = np.load(metadata_path, allow_pickle=True).tolist()
        
        
        

