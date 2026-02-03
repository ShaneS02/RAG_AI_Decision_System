#Takes the normalized ouput from the ingestion phase and splits the text into smaller chunks

from typing import List, Dict, Callable

def chunk_text(
    text: str, # The text to be chunked
    tokenize_fn: Callable[[str], List], # Function to tokenize text into a list of tokens
    target_tokens: int = 500, # Desired number of tokens per chunk
    max_tokens: int = 800, # Maximum allowed tokens per chunk
    overlap_tokens: int = 50, # Number of overlapping tokens between chunks
    min_tokens: int = 100 # Minimum number of tokens required to form a chunk
) -> List[Dict]:
    
    if not text.strip():
        return []
    
    # Split text into paragraphs and clean up whitespace
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    
    chunks = [] # List to hold the final chunks
    current_chunk_texts: List[str] = [] # Texts in the current chunk
    current_token_count = 0 # Current number of tokens in the chunk

    # Helper function to count tokens in a given text
    def count_tokens(txt: str) -> int:
        return len(tokenize_fn(txt))

    # Helper function to finalize and store the current chunk
    def flush_chunk():
        nonlocal current_chunk_texts, current_token_count
        
        if not current_chunk_texts:
            return
        
        # Finalize the current chunk
        chunk_text = " ".join(current_chunk_texts)
        chunks.append({
                "text": chunk_text,
                "token_count": current_token_count
            })

        # Reset current chunk and prepare overlap
        if overlap_tokens > 0:
            words = chunk_text.split()
            overlap_text = " ".join(words[-overlap_tokens:]) # Get last 'overlap_tokens' words
            current_chunk_texts = [overlap_text] # Start new chunk with overlap
            current_token_count = count_tokens(overlap_text) # Update token count
        else: 
            current_chunk_texts = []
            current_token_count = 0

    for paragraph in paragraphs:
        paragraph_token_count = count_tokens(paragraph) 

        #fallback for very large paragraphs
        if paragraph_token_count > max_tokens:
            flush_chunk() # Finalize current chunk before handling large paragraph

            words = paragraph.split()
            window_start_position = 0

            # Sliding window approach for large paragraphs
            while window_start_position < len(words):
                window_text = " ".join(words[window_start_position:window_start_position + target_tokens])
                chunks.append({
                    "text": window_text,  
                    "token_count": count_tokens(window_text)
                })
                
                # Move start index forward with overlap consideration
                window_start_position += target_tokens - overlap_tokens 
            
            continue # Move to the next paragraph
        
        # Check if adding the paragraph exceeds target tokens and finalize chunk if needed
        if current_token_count + paragraph_token_count > target_tokens:
            flush_chunk()

        current_chunk_texts.append(paragraph)
        current_token_count += paragraph_token_count
            
    flush_chunk() # Final flush for any remaining text

    #merge small chunks

    merged_chunks = [] 
    buffer = None #buffer represents the current chunk being built
    chunk_id = 1

    for chunk in chunks:
        if chunk["token_count"] < min_tokens and buffer:
            buffer["text"] += " " + chunk["text"]
            buffer["token_count"] += chunk["token_count"]
        else:
            if buffer:
                buffer["chunk_id"] = chunk_id
                chunk_id += 1
                merged_chunks.append(buffer) # Finalize and store the buffer chunk
            buffer = chunk 
    
    # Finalize any remaining buffer chunk
    if buffer:
        merged_chunks.append(buffer)

    return merged_chunks # Return the final list of all chunks