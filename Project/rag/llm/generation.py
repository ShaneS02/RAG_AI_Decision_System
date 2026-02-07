from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from .base import GenerationModel

class HFLocalGenerationModel(GenerationModel):
    """
    This wrapper handles:
    - Loading the model & tokenizer
    - Converting text prompts to token IDs
    - Generating text outputs
    - Decoding outputs to strings

    This design keeps the generation logic separate from the pipeline.
    """

    def __init__(
        self,
        model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device: str | None = None,
        max_new_tokens: int = 512,
        temperature: float = 0.0,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name) # Load the tokenizer matching the model
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        )

        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
 
    """
    Generate text given a prompt.
    Args: Input text to generate from.
    Returns: Generated string output from the model.
    """

    def generate(self, prompt: str) -> str:
        # Tokenize the input prompt and move to the device. "pt" - return pytorch tensor
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        # Disable gradient computation for inference
        with torch.no_grad():
            # Generate output token IDs
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                do_sample=self.temperature > 0,  # deterministic if temperature=0
                pad_token_id=self.tokenizer.eos_token_id  # ensures proper padding/eos handling
            )

        # Decode token IDs back to text, skipping special tokens
        return self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True
        )