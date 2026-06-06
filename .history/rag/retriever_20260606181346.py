from embedding_model import model


class Retriever:

    def __init__(self, chunks, store):

        self.chunks = chunks
        self.store = store

    def retrieve(self, query, k=5):

        query_embedding = model.encode(query)

        indices, distances = self.store.search(
            query_embedding,
            k
        )

        results = []

        for idx in indices:
            results.append(
                self.chunks[idx]
            )

        return results