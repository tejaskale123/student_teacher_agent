from sentence_transformers import SentenceTransformer

# Load only once
_model = None


def get_model():

    global _model

    if _model is None:

        print("Loading embedding model...")

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


def create_embeddings(chunks):

    model = get_model()

    embeddings = model.encode(
        chunks,
        show_progress_bar=False
    )

    return embeddings