from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

STOP_WORDS = {
    "the", "a", "an", "and",
    "of", "to", "in", "on", "for",
    "with", "me", "show", "find", "summarize",
}

def retrieve_records(records, question, searchable_fields):
    keywords = extract_keywords(question)

    scored_records = []

    for record in records:

        score = 0

        for field in searchable_fields:

            field_words = [
                stemmer.stem(word)
                for word in record.get(field, "").lower().split()
            ]

            for keyword in keywords:
                if keyword in field_words:
                    score += 1

        if score > 0:
            scored_records.append((score, record))

    scored_records.sort(reverse=True, key=lambda item: item[0])

    return [record for score, record in scored_records]


def extract_keywords(question):
    """
    Return meaningful keywords from the user's question.
    """

    words = question.lower().split()

    return [
        stemmer.stem(word.strip(".,?!"))
        for word in words
        if word.strip(".,?!") not in STOP_WORDS
    ]