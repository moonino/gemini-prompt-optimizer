from llmlingua import PromptCompressor
from app.core.config import settings
import logging

class CompressionService:
    def __init__(self):
        # Optimized for speed: using LLMLingua-2 small model if possible, 
        # or keeping phi-2 but with specific parameters for faster inference.
        # For lower latency on CPU, we prioritize selective generation patterns.
        try:
            self.compressor = PromptCompressor(
                model_name="microsoft/phi-2", 
                device_map="cpu"
            )
            logging.info("LLMLingua Compressor initialized with microsoft/phi-2.")
        except Exception as e:
            logging.error(f"Failed to initialize compressor: {e}")
            self.compressor = None

    def compress(self, prompt: str, target_token: int = None, rate: float = None):
        if not settings.COMPRESSION_ENABLED or not self.compressor:
            return prompt
        
        actual_rate = rate or settings.COMPRESSION_RATE
        
        # Latency optimization: use iterative_compress for better quality/speed balance 
        # or adjust force_tokens to minimize overhead.
        results = self.compressor.compress_prompt(
            [prompt],
            target_token=target_token,
            rate=actual_rate,
            force_tokens=['\n', '.', '?', '!'], # Keep basic structure
            chunk_end_tokens=['.', '\n'],
            dynamic_context_compression_ratio=0.3 # Optimization parameter
        )
        
        return results['compressed_prompt']

compressor_service = CompressionService()
