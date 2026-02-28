from sentence_transformers import SentenceTransformer

def get_embeddings(text_list, model_name='all-MiniLM-L6-v2'):
    """
    Generate embeddings for a list of texts using SentenceTransformer.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(text_list, show_progress_bar=True)
    return embeddings
