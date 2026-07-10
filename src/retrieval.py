from embedding_client import get_embedding, get_embeddings
from chroma_client import query_records, add_records

def retrieve_records(question):

    question_embedding = get_embedding(question)

    results = query_records(
        question_embedding.tolist(),
    )

    return results["metadatas"][0]


def build_search_text(record, searchable_fields):
    """
    Combine searchable fields into one string.
    """
    values = [
        record.get(field, "")
        for field in searchable_fields
    ]

    return " ".join(values)

def build_chroma_index(records, searchable_fields, batch_size=256):
    """
    Embed records in batches and store them in Chroma.
    """

    total = len(records)

    for start in range(0, total, batch_size):

        end = min(start + batch_size, total)

        batch = records[start:end]

        documents = []
        ids = []
        metadatas = []

        for record in batch:

            search_text = build_search_text(
                record,
                searchable_fields,
            )

            documents.append(search_text)

            ids.append(str(record["record_id"]))

            metadatas.append(record)

        embeddings = get_embeddings(documents).tolist()

        add_records(
            ids,
            embeddings,
            documents,
            metadatas,
        )

        print(f"Indexed {end}/{total}")