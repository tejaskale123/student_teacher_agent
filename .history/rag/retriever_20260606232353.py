from sentence_transformers import SentenceTransformer


class Retriever:

    def __init__(self, chunks, store):

        self.chunks = chunks
        self.store = store

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def retrieve(self, query, k=5):

        query_embedding = self.model.encode(
            query,
            show_progress_bar=False
        )

        indices, distances = self.store.search(
            query_embedding,
            k
        )

        results = []

        for idx in indices:

            if 0 <= idx < len(self.chunks):

                results.append(
                    self.chunks[idx]
                )

        return results