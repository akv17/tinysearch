import numpy as np
from ...data import Score


def rank_ids_by_scores(ids, scores, k=1):
    mask = np.argsort(scores)
    mask = mask[-k:][::-1]
    scores = scores[mask]
    scores = scores.tolist()
    ids = ids[mask].tolist()
    scores = [Score(id=i, score=s) for i, s in zip(ids, scores)]
    return scores
