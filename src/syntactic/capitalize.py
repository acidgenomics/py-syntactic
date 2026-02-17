"""Capitalize and sentence case functions."""

import re


def capitalize(obj: str | list[str], strict: bool = False) -> list[str]:
    """Capitalize the first letter of each string.

    When strict=True, lowercases the remaining characters.
    """
    if isinstance(obj, str):
        obj = [obj]
    result = []
    for s in obj:
        if not s:
            result.append(s)
            continue
        first = s[0].upper()
        tail = s[1:]
        if strict:
            tail = tail.lower()
        result.append(first + tail)
    return result


def sentence_case(obj: str | list[str], strict: bool = False) -> list[str]:
    """Convert strings to sentence case.

    Capitalizes the first letter of the first word. Subsequent words are
    lowercased unless they appear to be acronyms (all-caps, mixed case with
    multiple uppercase letters, etc.).

    When strict=True, forces ALL words (including first) to title/lowercase.
    """
    if isinstance(obj, str):
        obj = [obj]
    result = []
    for s in obj:
        if " " not in s:
            result.append(s)
            continue
        words = s.split(" ")
        if strict:
            # In strict mode, first word: capitalize first letter, lowercase rest
            first_word = words[0][0].upper() + words[0][1:].lower() if words[0] else ""
            other_words = [w.lower() for w in words[1:]]
        else:
            first_word = words[0][0].upper() + words[0][1:] if words[0] else ""
            other_words = []
            for word in words[1:]:
                if (
                    re.match(r"^[.A-Z0-9]+$", word)
                    or re.search(r"[.a-z0-9][A-Z]", word)
                    or re.search(r"[A-Z]{2}", word)
                ):
                    other_words.append(word)
                else:
                    other_words.append(word.lower())
        result.append(" ".join([first_word] + other_words))
    return result
