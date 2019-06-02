import unicodedata

def normalized_word(string_of_word):
    nikudnik = str(string_of_word)
    normalized = unicodedata.normalize('NFKD', nikudnik)
    flattened = "".join([c for c in normalized if not unicodedata.combining(c)])
    return flattened
