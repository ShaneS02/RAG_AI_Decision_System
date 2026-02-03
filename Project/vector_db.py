import faiss
import numpy as np

from typing import Dict, List
from .chunk_validator import Chunk

class VectorDatabase:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.dim = embedding_service.get_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dim) # Create a FAISS index
        self.metadata = []  # list of dicts corresponding to each vector
    
    #ensure chunks are properly formatted and consists of the required keys
    def _validate_chunk(self, formatted):
        try:
            Chunk(**formatted) #validate proper chunk formatting
        except Exception as e:
            raise ValueError(f"Chunk validation failed: {e}")
            
        
    #properly format chunks
    def prepare_chunks(self, document: Dict, chunks: List):
        prepared_chunks = []

        for chunk in chunks:
            # Store chunk with metadata
            formatted = {
                "document_id": document["id"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "file_name": document["file_name"], 
                "source": document["source"],
                "metadata": document["metadata"],
                "created_at": document["ingested_at"],
                "citation": f"{document["file_name"]}#chunk{chunk["chunk_id"]}"
            }

            #raises an exception if format is incorrect
            self._validate_chunk(formatted)
            
            #if valid, append
            prepared_chunks.append(formatted)
            
        return prepared_chunks

    # Add chunks to the FAISS index
    def add_chunks(self, chunks : List[Dict]):
        for chunk in chunks:
            self._validate_chunk(chunk) #raises an exception if format is incorrect

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
        
        
        

