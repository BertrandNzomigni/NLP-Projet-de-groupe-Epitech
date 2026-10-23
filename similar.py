from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tokenizer import tokenize
from manager import cache_reader, cache_writer
import os
import numpy as np
import pandas

def similarity(id):
    model = SentenceTransformer("all-mpnet-base-v2")  # better model

    books_list = [11,12,16,55,113,120,236,108,834,1661,61262,69087,70114,35,36,84,159,164,345,68283]
    if id in books_list:
        books_list.remove(id)
    books_list.append(id)

    texts = []
    for book in books_list:
        if os.path.exists(f"cache/tokenize/tokenize_{book}.json"):
            sentences = cache_reader(f"tokenize/tokenize_{book}")
        else:
            sentences = tokenize(book, False)

        # Join first 200 sentences into one text block per book
        texts.append(" ".join(sentences[:200]))

    embeddings = model.encode(texts, show_progress_bar=True, batch_size=16)
    sim = cosine_similarity(embeddings)

    catalog = pandas.read_csv('pg_catalog.csv')

    result = top_similar(sim, books_list, id, top_n=5)
    result2 = [
        (book_id, catalog[catalog["Text#"] == book_id].iloc[0]["Title"])
        for book_id, score in result
    ]
    cache_writer(f"similarity/similar_{id}", result2)
    return result2


def top_similar(sim_matrix, books_list, id, top_n=5):
    query_idx = len(books_list) - 1
    scores = sim_matrix[query_idx]

    ranked = np.argsort(scores)[::-1]
    ranked = [i for i in ranked if i != query_idx][:top_n]

    return [(books_list[i], round(float(scores[i]), 4)) for i in ranked]