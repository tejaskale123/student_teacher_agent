import faiss
import numpy as np
import os


class VectorStore:

    def __init__(self, embeddings=None):

        self.index = None

        if embeddings is not None:

            self.index = faiss.IndexFlatL2(
                embeddings.shape[1]
            )

            self.index.add(
                np.array(
                    embeddings
                ).astype("float32")
            )

    def save(self, path="faiss_index.bin"):

        faiss.write_index(
            self.index,
            path
        )

    def load(self, path="faiss_index.bin"):

        self.index = faiss.read_index(
            path
        )

    def exists(self, path="faiss_index.bin"):

        return os.path.exists(path)

    def search(self, query_embedding, k=5):

        distances, indices = self.index.search(
            np.array(
                [query_embedding]
            ).astype("float32"),
            k
        )

        return indices[0], distances[0]