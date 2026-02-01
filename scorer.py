from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def score_answer(candidate_answer, ideal_answer, time_taken, max_time):
    emb1 = model.encode([candidate_answer])
    emb2 = model.encode([ideal_answer])

    similarity = cosine_similarity(emb1, emb2)[0][0]

    accuracy = similarity * 30
    clarity = min(len(candidate_answer.split()) / 50, 1) * 15
    depth = similarity * 20
    relevance = similarity * 20
    time_eff = (1 - time_taken / max_time) * 15

    total = accuracy + clarity + depth + relevance + time_eff
    return round(total, 2)
