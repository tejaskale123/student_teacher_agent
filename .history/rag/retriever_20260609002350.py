from rag.embedding_model import get_model
from sentence_transformers import CrossEncoder


_reranker = None


def get_reranker():

    global _reranker

    if _reranker is None:

        print("Loading reranker model...")

       self.reranker = CrossEncoder(
           "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    return _reranker


class Retriever:

    def __init__(self, chunks, store):

        self.chunks = chunks
        self.store = store

        self.model = get_model()
        self.reranker = None

    def retrieve(self, query, k=3):

        query_embedding = self.model.encode(
            query,
            show_progress_bar=False
        )

        indices, distances = self.store.search(
            query_embedding,
            10
        )

        candidates = []

        for idx in indices:

            if 0 <= idx < len(self.chunks):

                candidates.append(
                    self.chunks[idx]
                )

        if len(candidates) <= k:
            return candidates

        try:
            if self.reranker is None:
                self.reranker = get_reranker()

            pairs = [
                (query, chunk)
                for chunk in candidates
            ]

            scores = self.reranker.predict(
                pairs
            )

            ranked = sorted(
                zip(
                    candidates,
                    scores
                ),
                key=lambda x: x[1],
                reverse=True
            )

            return [
                chunk
                for chunk, score
                in ranked[:k]
            ]

        except Exception as error:
            print("Reranker fallback:", error)
            return candidates[:k]
