from embedding_model import create_embeddings


class Retriever:

    def __init__(self, chunks, vector_store):

        self.chunks = chunks
        self.vector_store = vector_store

    def retrieve(self, question, k=3):

        query_embedding = create_embeddings(
            [question]
        )[0]

        indices = self.vector_store.search(
            query_embedding,
            k
        )

        results = []

        for idx in indices:

            results.append(
                self.chunks[idx]
            )

        return results