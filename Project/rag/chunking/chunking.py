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
        return len(tokenize_fn(txt)["input_ids"])

    # Helper function to finalize and store the current chunk
    def flush_chunk():
        nonlocal current_chunk_texts, current_token_count
        
        if not current_chunk_texts:
            return
        
        # Finalize the current chunk
        chunk_text = " ".join(current_chunk_texts)
        chunk_tokens = tokenize_fn(chunk_text)["input_ids"]
        chunks.append({
                "text": chunk_text,
                "token_count": len(chunk_tokens)
            })

        # Reset current chunk and prepare overlap
        if overlap_tokens > 0:
            overlap_token_ids = chunk_tokens[-overlap_tokens:]
            overlap_text = tokenize_fn.decode(overlap_token_ids)

            current_chunk_texts = [overlap_text] # Start new chunk with overlap
            current_token_count = len(overlap_token_ids) # Update token count
        else: 
            current_chunk_texts = []
            current_token_count = 0

    for paragraph in paragraphs:
        paragraph_token_count = count_tokens(paragraph) 

        #fallback for very large paragraphs
        print(f"Paragraph token count too big: {paragraph_token_count}, Enforcing toekn limit of {max_tokens}")
        if paragraph_token_count > max_tokens:
            flush_chunk() # Finalize current chunk before handling large paragraph

            # Sliding window approach for large paragraphs
            tokens = tokenize_fn(paragraph)["input_ids"]
            start = 0
            while start < len(tokens):
                chunk_tokens = tokens[start:start + target_tokens]
                chunk_text = tokenize_fn.decode(chunk_tokens)
                chunks.append({
                    "text": chunk_text,  
                    "token_count": len(chunk_tokens)
                })
                
                # Move start index forward with overlap consideration
                start += target_tokens - overlap_tokens
            
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

    print("merging small chunks if needed")
    for chunk in chunks:
        if not chunk["text"].strip():  # skip empty text
            continue

        if buffer is None:
            buffer = chunk
            continue

        new_token_count = buffer["token_count"] + chunk["token_count"]
        if (chunk["token_count"] < min_tokens and buffer ) and new_token_count <= max_tokens:
            buffer["text"] += " " + chunk["text"]
            buffer["token_count"] += chunk["token_count"]
        else:
            if buffer:
                buffer["chunk_id"] = chunk_id
                chunk_id += 1
                merged_chunks.append(buffer) # Finalize and store the buffer chunk
            buffer = chunk 
    
    # Finalize any remaining buffer chunks
    print("finalizing remaining buffer chunk if exists")
    if buffer:
        buffer["chunk_id"] = chunk_id
        merged_chunks.append(buffer)

    print(f"Total chunks created: {len(merged_chunks)}")
    return merged_chunks # Return the final list of all chunks