"""Make human-readable words, labels, and titles from variable names."""

import re

from syntactic._engine import _syntactic
from syntactic.capitalize import sentence_case


def make_words(obj: str | list[str]) -> list[str]:
    """Convert variable names to human-readable word strings.

    Strings that already contain spaces are returned unmodified.
    """
    if isinstance(obj, str):
        obj = [obj]
    result = []
    for s in obj:
        if re.search(r"\s", s):
            result.append(s)
            continue
        processed = _syntactic([s])[0]
        processed = re.sub(r"[_.]+", " ", processed)
        # Convert single uppercase letters to lowercase.
        processed = re.sub(
            r"\b([A-Z])\b",
            lambda m: m.group(1).lower(),
            processed,
        )
        # Convert capitalized words (not all-caps acronyms) to lowercase.
        processed = re.sub(
            r"\b([A-Z][a-z0-9]+)\b",
            lambda m: m.group(1).lower(),
            processed,
        )
        # Include period for versus.
        processed = re.sub(r"\b(v|vs)\b", r"\1.", processed)
        result.append(processed)
    return result


def make_title(obj: str | list[str]) -> list[str]:
    """Convert variable names to title-cased strings.

    Applies makeWords then sentenceCase to each string.
    """
    if isinstance(obj, str):
        obj = [obj]
    words_list = make_words(obj)
    return sentence_case(words_list)


def make_label(obj: str | list[str]) -> list[str]:
    """Convert variable names to human-readable labels.

    Applies makeWords and capitalizes the first letter of the result.
    """
    if isinstance(obj, str):
        obj = [obj]
    words_list = make_words(obj)
    result = []
    for w in words_list:
        if w:
            result.append(w[0].upper() + w[1:])
        else:
            result.append(w)
    return result
