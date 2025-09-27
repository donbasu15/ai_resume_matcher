from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

# Load models with error handling
try:
    # Use a more robust model for better embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("SentenceTransformer model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load SentenceTransformer model: {e}")
    model = None

def get_embedding(text: str):
    """Generate embedding for text using SentenceTransformer."""
    if not model:
        raise RuntimeError("SentenceTransformer model not available")
    
    if not text or not text.strip():
        # Return zero embedding for empty text
        return torch.zeros(384)  # MiniLM-L6-v2 has 384 dimensions
    
    try:
        return model.encode(text, convert_to_tensor=True)
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return torch.zeros(384)

def compute_similarity(resume_text: str, jd_text: str) -> float:
    """Return cosine similarity between resume and job description."""
    try:
        if not resume_text.strip() or not jd_text.strip():
            return 0.0
        
        resume_emb = get_embedding(resume_text)
        jd_emb = get_embedding(jd_text)
        
        score = util.pytorch_cos_sim(resume_emb, jd_emb)
        return round(float(score) * 100, 2)
    
    except Exception as e:
        logger.error(f"Error computing similarity: {e}")
        # Fallback to TF-IDF based similarity
        return compute_tfidf_similarity(resume_text, jd_text)

def compute_tfidf_similarity(text1: str, text2: str) -> float:
    """Fallback similarity computation using TF-IDF."""
    try:
        if not text1.strip() or not text2.strip():
            return 0.0
        
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        
        # Fit and transform the texts
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        
        # Compute cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        return round(float(similarity[0][0]) * 100, 2)
    
    except Exception as e:
        logger.error(f"Error computing TF-IDF similarity: {e}")
        return 0.0

def compute_semantic_similarity_detailed(text1: str, text2: str) -> dict:
    """Compute detailed semantic similarity metrics."""
    try:
        # Basic similarity
        basic_sim = compute_similarity(text1, text2)
        
        # TF-IDF similarity for comparison
        tfidf_sim = compute_tfidf_similarity(text1, text2)
        
        # Sentence-level similarity (if texts are long enough)
        sentences1 = [s.strip() for s in text1.split('.') if s.strip()]
        sentences2 = [s.strip() for s in text2.split('.') if s.strip()]
        
        sentence_similarities = []
        if len(sentences1) > 0 and len(sentences2) > 0 and model:
            # Compute similarity between all sentence pairs
            for s1 in sentences1[:5]:  # Limit to first 5 sentences
                for s2 in sentences2[:5]:
                    if s1 and s2:
                        sim = compute_similarity(s1, s2)
                        sentence_similarities.append(sim)
        
        avg_sentence_sim = np.mean(sentence_similarities) if sentence_similarities else basic_sim
        max_sentence_sim = max(sentence_similarities) if sentence_similarities else basic_sim
        
        return {
            'overall_similarity': basic_sim,
            'tfidf_similarity': tfidf_sim,
            'avg_sentence_similarity': round(avg_sentence_sim, 2),
            'max_sentence_similarity': round(max_sentence_sim, 2),
            'similarity_confidence': min(basic_sim, tfidf_sim) / max(basic_sim, tfidf_sim, 1) * 100
        }
    
    except Exception as e:
        logger.error(f"Error computing detailed similarity: {e}")
        return {
            'overall_similarity': 0.0,
            'tfidf_similarity': 0.0,
            'avg_sentence_similarity': 0.0,
            'max_sentence_similarity': 0.0,
            'similarity_confidence': 0.0
        }

def batch_similarity(texts: list, reference_text: str) -> list:
    """Compute similarity for multiple texts against a reference text."""
    if not model or not texts or not reference_text:
        return [0.0] * len(texts)
    
    try:
        # Generate embeddings for all texts
        text_embeddings = model.encode(texts, convert_to_tensor=True)
        ref_embedding = model.encode(reference_text, convert_to_tensor=True)
        
        # Compute similarities
        similarities = util.pytorch_cos_sim(text_embeddings, ref_embedding)
        
        return [round(float(sim) * 100, 2) for sim in similarities.flatten()]
    
    except Exception as e:
        logger.error(f"Error in batch similarity computation: {e}")
        return [compute_similarity(text, reference_text) for text in texts]
