def remove_empty_fields(record):
    """
    Return a copy of the record with empty-string fields removed.
    """
    return {
        key: value
        for key, value in record.items()
        if value != ""
    }