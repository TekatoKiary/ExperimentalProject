import string

__all__ = []

SAME_LETTERS = {
    "o": "0",
    "о": "0",
    "c": "с",
    "e": "е",
    "p": "р",
    "t": "т",
    "a": "а",
    "y": "у",
    "x": "х",
    "m": "м",
    "h": "н",
    "k": "к",
    "з": "3",
}


def normalize_data(value):
    value = "".join(
        [
            SAME_LETTERS[i] if i in SAME_LETTERS else i
            for i in " ".join(value.lower().split())
        ],
    )
    for i in string.punctuation:
        value = "".join(value.split(i))
    return value
