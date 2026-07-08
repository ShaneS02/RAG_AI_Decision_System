from typing import List, Dict

class ChunkingModel:
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.chunks : List[Dict] = [] # List to hold the final chunks
        self.current_chunk_texts: List[str] = [] # Texts in the current chunk
        self.current_token_count = 0 # Current number of tokens in the chunk

    def add_chunk(self, text: str) -> List[Dict]:
        self.chunks.append({
                "text": text,
                "token_count": len(self.token_manager.tokenize(text))
            })
    
    # finalize the current chunk and prepare for the next one, considering overlap
    def _flush_chunk(self):
        
        if not self.current_chunk_texts:
            return
        
        # Finalize the current chunk
        chunk_text = " ".join(self.current_chunk_texts)
        self.add_chunk(chunk_text)

        # Reset current chunk and prepare overlap
        chunk_tokens = self.token_manager.tokenize(chunk_text)
        if self.token_manager.overlap_tokens > 0:
            overlap_token_ids = chunk_tokens[-self.token_manager.overlap_tokens:]
            overlap_text = self.token_manager.decode(overlap_token_ids)

            self.current_chunk_texts = [overlap_text] # Start new chunk with overlap
            self.current_token_count = len(overlap_token_ids) # Update token count
        else: 
            self.current_chunk_texts = []
            self.current_token_count = 0

    def chunk_remaining_text(self):
        self._flush_chunk()  # Finalize any remaining text as a chunk
        

    def split_text_into_chunks(self, text: str) -> List[Dict]:
        text_token_count = len(self.token_manager.tokenize(text))

        #fallback for very large block of text
        if text_token_count > self.token_manager.max_tokens:
            print(f"token count too big: {text_token_count}, Enforcing token limit of {self.token_manager.max_tokens}")
            self._flush_chunk() # Finalize current chunk before handling large paragraph

            # Sliding window approach for large block of text
            tokens = self.token_manager.tokenize(text)
            start = 0
            while start < len(tokens):
                chunk_tokens = tokens[start:start + self.token_manager.target_tokens]
                chunk_text = self.token_manager.decode(chunk_tokens)
                self.add_chunk(chunk_text)
                
                # Move start index forward with overlap consideration
                start += self.token_manager.target_tokens - self.token_manager.overlap_tokens
            
            return 
        
        # Check if adding the paragraph exceeds target tokens and finalize chunk if needed
        if self.current_token_count + text_token_count > self.token_manager.target_tokens:
            self._flush_chunk()

        self.current_chunk_texts.append(text)
        self.current_token_count += text_token_count


    def merge_small_chunks(self) -> List[Dict]:
        merged_chunks = [] 
        buffer = None #buffer represents the current chunk being built
        chunk_id = 1

        print("merging small chunks if needed")
        for chunk in self.chunks:
            if not chunk["text"].strip():  # skip empty text
                continue

            if buffer is None:
                buffer = chunk
                continue

            new_token_count = buffer["token_count"] + chunk["token_count"]
            if (chunk["token_count"] < self.token_manager.min_tokens and buffer ) and new_token_count <= self.token_manager.max_tokens:
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
        
        return merged_chunks


    