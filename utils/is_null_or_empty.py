def is_null_or_empty(x):  # Returns true if null or empty
    null_or_empty = False

    if not (x):  # checks for nulls
        null_or_empty = True
    if x.isspace():  # checks for blank strings
        null_or_empty = True

    return null_or_empty
