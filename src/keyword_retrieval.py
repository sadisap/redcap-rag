from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


vectorizer = TfidfVectorizer()

document_matrix = None
records = None


def build_keyword_index(documents, metadata):
    """
    Build a TF-IDF index for all searchable documents.
    """

    global document_matrix
    global records

    records = metadata
    document_matrix = vectorizer.fit_transform(documents)


def keyword_search(question, top_k=20):
    """
    Return the top TF-IDF matches for a question.
    """

    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(
        question_vector,
        document_matrix,
    )[0]

    ranked_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:

        results.append(
            {
                "id": str(records[index]["record_id"]),
                "record": records[index],
                "score": float(similarities[index]),
            }
        )

    return results