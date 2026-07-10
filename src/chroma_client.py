import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="redcap_records"
)


def add_records(ids, embeddings, documents, metadatas):
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query_records(question_embedding, top_k=5):
    """
    Return the most semantically similar records.
    """

    return collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )


def reset_collection():
    """
    Remove all records from the collection.
    """

    global collection

    client.delete_collection("redcap_records")

    collection = client.get_or_create_collection(
        name="redcap_records"
    )