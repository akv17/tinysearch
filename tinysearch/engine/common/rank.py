import numpy as np
from ...data import Score


def rank_ids_by_scores(ids, scores, k=1):
    """
    Ранжирует айди по значению метрики и возвращает k самых релевантных айди
    :param ids: список айди
    :param scores: список значений метрики
    :param k: величина k
    :return:
    """
    mask = np.argsort(scores)
    mask = mask[-k:][::-1]
    scores = scores[mask]
    scores = scores.tolist()
    ids = ids[mask].tolist()
    scores = [Score(id=i, score=s) for i, s in zip(ids, scores)]
    return scores
