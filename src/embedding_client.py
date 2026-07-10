from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    """
    Generate an embedding vector for the given text.
    """
    return model.encode(text)


def get_embeddings(texts):
    return model.encode(texts)