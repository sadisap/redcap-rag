from embedding_client import (
    get_embedding,
    get_embeddings,
)

from chroma_client import (
    query_records,
    add_records,
)

from keyword_retrieval import (
    keyword_search,
)


SEMANTIC_WEIGHT = 0.7
KEYWORD_WEIGHT = 0.3


def build_search_document(record, searchable_fields):
    """
    Construct the text representation of a REDCap record.
    """

    values = [
        record.get(field, "")
        for field in searchable_fields
    ]

    return "\n".join(values)


def build_documents(records, searchable_fields):
    """
    Build the semantic document for every REDCap record.

    Returns:
        documents: list[str]
        ids: list[str]
        metadata: list[dict]
    """

    documents = []
    ids = []
    metadata = []

    for record in records:

        document = build_search_document(
            record,
            searchable_fields,
        )

        documents.append(document)
        ids.append(str(record["record_id"]))
        metadata.append(record)

    return documents, ids, metadata


def build_chroma_index(
    documents,
    ids,
    metadata,
    batch_size=256,
):
    """
    Store pre-built documents in Chroma.
    """

    total = len(documents)

    for start in range(0, total, batch_size):

        end = min(start + batch_size, total)

        add_records(
            ids[start:end],
            get_embeddings(
                documents[start:end]
            ).tolist(),
            documents[start:end],
            metadata[start:end],
        )

        print(f"Indexed {end}/{total}")
        

def semantic_search(question, top_k=20):
    """
    Perform semantic retrieval using Chroma.
    """

    question_embedding = get_embedding(question)

    results = query_records(
        question_embedding.tolist(),
        top_k,
    )

    semantic_results = []

    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for record_id, metadata, distance in zip(
        ids,
        metadatas,
        distances,
    ):

        semantic_results.append(
            {
                "id": record_id,
                "record": metadata,
                "score": 1 - distance,
            }
        )

    return semantic_results


def normalize_scores(results):
    """
    Normalize scores to the range [0, 1].
    """

    if not results:
        return results

    scores = [r["score"] for r in results]

    minimum = min(scores)
    maximum = max(scores)

    if maximum == minimum:

        for result in results:
            result["score"] = 1.0

        return results

    for result in results:

        result["score"] = (
            result["score"] - minimum
        ) / (maximum - minimum)

    return results


def retrieve_records(question, top_k=5):
    """
    Hybrid retrieval using semantic + TF-IDF search.
    """

    semantic_results = normalize_scores(
        semantic_search(question, 20)
    )

    keyword_results = normalize_scores(
        keyword_search(question, 20)
    )

    combined = {}

    for result in semantic_results:

        combined[result["id"]] = {
            "record": result["record"],
            "semantic": result["score"],
            "keyword": 0,
        }

    for result in keyword_results:

        if result["id"] not in combined:

            combined[result["id"]] = {
                "record": result["record"],
                "semantic": 0,
                "keyword": result["score"],
            }

        else:

            combined[result["id"]]["keyword"] = result["score"]

    ranked = []

    for value in combined.values():

        score = (
            SEMANTIC_WEIGHT * value["semantic"]
            + KEYWORD_WEIGHT * value["keyword"]
        )

        ranked.append(
            {
                "record": value["record"],
                "score": score,
            }
        )

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return [
        item["record"]
        for item in ranked[:top_k]
    ]