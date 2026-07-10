from redcap_client import get_records
from retrieval import retrieve_records
from utils import remove_empty_fields
from llm_client import ask_llm


def main():
    records = get_records()

    question = "Summarize the Mock OR and tour activities represented in these records."

    searchable_fields = [
        "mot_title_or_description",
    ]

    retrieved_records = retrieve_records(
        records,
        question,
        searchable_fields,
    )

    clean_records = [
        remove_empty_fields(record)
        for record in retrieved_records[:5]
    ]

    print(f"Retrieved {len(clean_records)} records.\n")

    for record in clean_records:
        print(record)


if __name__ == "__main__":
    main()