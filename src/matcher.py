from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(resume_embeddings, jd_embedding):
    """
    Calculate cosine similarity between resume embeddings and JD embedding.
    """
    # jd_embedding should be (1, N), resume_embeddings should be (M, N)
    if len(jd_embedding.shape) == 1:
        jd_embedding = jd_embedding.reshape(1, -1)
    
    similarities = cosine_similarity(resume_embeddings, jd_embedding)
    return similarities.flatten()
