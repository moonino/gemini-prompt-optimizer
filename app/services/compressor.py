import re
import math
import logging
from typing import Dict, Any
import networkx as nx
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from app.core.config import settings

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)

class CompressionService:
    def __init__(self):
        logging.info("Initialized Lightweight NLP Compressor (Regex + NLTK + TextRank)")
        
        # Load English stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = set(['the', 'is', 'in', 'at', 'of', 'on', 'and', 'a', 'to', 'for'])

        # Basic Korean Stopwords (Custom list since NLTK doesn't provide it by default)
        self.korean_stopwords = {
            '은', '는', '이', '가', '을', '를', '의', '에', '에게', '에서', '으로', '로', '와', '과', 
            '도', '만', '까지', '마저', '조차', '부터', '입니다', '습니다', '하고', '수', '있는', 
            '하는', '그리고', '하지만', '그런데', '따라서', '알려줘', '부탁해', '안녕하세요', '감사합니다'
        }

    def _estimate_tokens(self, text: str) -> int:
        """Roughly estimate token count (1 token ≈ 4 characters for English/Korean mix)"""
        return max(1, len(text) // 4)

    def _regex_clean(self, text: str) -> str:
        """Step 1: Clean excessive whitespaces and unnecessary formatting."""
        # Remove consecutive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove markdown headers formatting characters if they don't contain content
        text = re.sub(r'#+\s*(?=\n|$)', '', text)
        # Remove redundant spaces
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()

    def _remove_stopwords(self, text: str) -> str:
        """Step 2: Remove common stopwords to save tokens without losing core meaning."""
        # Simple whitespace based tokenization to preserve punctuation attached to meaningful words
        words = text.split()
        cleaned_words = []
        for w in words:
            # Strip simple punctuation to check against stopwords properly
            check_w = re.sub(r'[^\w\s]', '', w.lower())
            if check_w in self.stop_words or check_w in self.korean_stopwords:
                continue
            cleaned_words.append(w)
        return " ".join(cleaned_words)

    def _textrank_summarize(self, text: str, target_ratio: float) -> str:
        """Step 3: NetworkX based TextRank for extractive summarization of long docs."""
        try:
            sentences = sent_tokenize(text)
        except Exception:
            # Fallback if punk tokenization fails
            sentences = [s.strip() for s in re.split(r'[.!?]\s+', text) if s.strip()]

        # If it's too short, don't summarize via TextRank
        if len(sentences) < 4:
            return text

        target_sentences_count = max(1, int(len(sentences) * target_ratio))
        
        # Jaccard similarity between sentences
        def jaccard(s1, s2):
            w1, w2 = set(s1.split()), set(s2.split())
            if not w1 or not w2:
                return 0.0
            intersection = len(w1.intersection(w2))
            union = len(w1.union(w2))
            return intersection / union if union > 0 else 0.0

        graph = nx.Graph()
        graph.add_nodes_from(range(len(sentences)))
        
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                sim = jaccard(sentences[i], sentences[j])
                if sim > 0:
                    graph.add_edge(i, j, weight=sim)
                    
        try:
            # Calculate PageRank
            scores = nx.pagerank(graph, weight='weight', max_iter=50)
            
            # Sort sentences by score descending
            ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
            
            # Select top target sentences
            top_sentences = [s for _, s in ranked[:target_sentences_count]]
            
            # Preserve original chronological order
            ordered_summary = [s for s in sentences if s in top_sentences]
            return " ".join(ordered_summary)
        except Exception as e:
            logging.warning(f"TextRank graph convergence failed: {e}. Falling back to simple truncation.")
            return " ".join(sentences[:target_sentences_count])

    def compress(self, prompt: str, target_token: int | None = None, rate: float | None = None) -> Dict[str, Any]:
        """Main compression pipeline entry point."""
        original_token_estimate = self._estimate_tokens(prompt)
        
        if not settings.COMPRESSION_ENABLED:
            return {
                "compressed_prompt": prompt,
                "origin_tokens": original_token_estimate,
                "compressed_tokens": original_token_estimate
            }
            
        actual_rate = rate or settings.COMPRESSION_RATE
        
        try:
            # 1. Regex Cleaning (very safe)
            cleaned = self._regex_clean(prompt)
            
            # 2. TextRank Summary (if long enough)
            if len(cleaned) > 200:
                summarized = self._textrank_summarize(cleaned, actual_rate + 0.1) # Add slight buffer 
            else:
                summarized = cleaned
                
            # 3. Stopword removal (last step polish)
            final_text = self._remove_stopwords(summarized)
                
            # Failsafe: if we somehow stripped everything (e.g., prompt was literally just "hello")
            if len(final_text.strip()) == 0:
                final_text = prompt

            compressed_token_estimate = self._estimate_tokens(final_text)

            return {
                "compressed_prompt": final_text,
                "origin_tokens": original_token_estimate,
                "compressed_tokens": compressed_token_estimate
            }

        except Exception as e:
            logging.error(f"NLP Compression pipeline failed: {e}")
            return {
                "compressed_prompt": prompt,
                "origin_tokens": original_token_estimate,
                "compressed_tokens": original_token_estimate
            }

compressor_service = CompressionService()
