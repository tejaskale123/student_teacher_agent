import faiss
import numpy as np


class VectorStore:

    def __init__(self, embeddings):

        self.index = faiss.IndexFlatL2(
            embeddings.shape[1]
        )

        self.index.add(
            np.array(embeddings).astype("float32")
        )

    def search(self, query_embedding, k=3):

        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        return indices[0]