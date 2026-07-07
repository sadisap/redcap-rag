def remove_empty_fields(record):
    """
    Return a copy of the record with empty-string fields removed.
    """
    return {
        key: value
        for key, value in record.items()
        if value != ""
    }


def filter_records(records, field_name):
    """
    Return records where the specified field is not empty.
    """
    return [
        record
        for record in records
        if record.get(field_name, "") != ""
    ]