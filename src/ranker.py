def rank_candidates(candidates_data):
    """
    candidates_data: list of dicts with 'name', 'score', 'skills', etc.
    Sort by score descending.
    """
    ranked_list = sorted(candidates_data, key=lambda x: x['score'], reverse=True)
    return ranked_list
