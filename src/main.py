from redcap_client import get_records
from retrieval import (
    build_chroma_index,
    retrieve_records,
)
from utils import remove_empty_fields
from llm_client import ask_llm
from chroma_client import reset_collection


def main():
    records = get_records()

    question = "Summarize the Mock OR and tour activities represented in these records."

    searchable_fields = [
        "mot_title_or_description",
    ]

    reset_collection()

    build_chroma_index(
        records,
        searchable_fields,
    )

    retrieved_records = retrieve_records(
        question,
    )

    clean_records = [
        remove_empty_fields(record)
        for record in retrieved_records
    ]

    answer = ask_llm(clean_records, question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()