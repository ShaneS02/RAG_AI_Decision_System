#Takes the normalized ouput from the ingestion phase and splits the text into smaller chunks

from typing import List, Dict
from .token_model import TokenManager
from .chunking_model import ChunkingModel

def chunk_text(text: str, token_manager: TokenManager) -> List[Dict]:
    
    if not text.strip():
        return []
    
    # Split text into paragraphs and clean up whitespace
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    
    chunker = ChunkingModel(token_manager=token_manager)

    for paragraph in paragraphs:
        chunker.split_text_into_chunks(paragraph)
            
    chunker.chunk_remaining_text()

    #merge small chunks
    merged_chunks = chunker.merge_small_chunks()
    

    print(f"Total chunks created: {len(merged_chunks)}")
    return merged_chunks # Return the final list of all chunks

