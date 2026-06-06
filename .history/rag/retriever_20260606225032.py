from embedding_model import model


class Retriever:

    def __init__(self, chunks, store):

        self.chunks = chunks
        self.store = store

    def retrieve(self, query, k=5):

        # Convert question into embedding
        query_embedding = model.encode(query)

        # Search FAISS index
        indices, distances = self.store.search(
            query_embedding,
            k
        )

        results = []

        # Get matching chunks
        for idx in indices:

            if idx < len(self.chunks):

                results.append(
                    self.chunks[idx]
                )

        return results