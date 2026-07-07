from redcap_client import get_records
from utils import filter_records, remove_empty_fields
from llm_client import ask_llm


def main():
    records = get_records()

    mot_records = filter_records(
        records,
        "mot_title_or_description",
    )

    clean_records = [
        remove_empty_fields(record)
        for record in mot_records[:5]
    ]

    question = "Summarize the Mock OR and tour activities represented in these records."

    answer = ask_llm(clean_records, question)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()