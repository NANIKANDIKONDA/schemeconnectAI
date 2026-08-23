from sentence_transformers import SentenceTransformer

# Load the model only once
MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def get_model():
    global _model
    if _model is None:
        try:
            _model = SentenceTransformer(MODEL_NAME)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            raise
    return _model

def embed_text(text: str) -> list[float]:
    """Embeds a single string into a vector."""
    model = get_model()
    return model.encode(text).tolist()

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embeds a list of strings into a list of vectors."""
    model = get_model()
    return model.encode(texts).tolist()
