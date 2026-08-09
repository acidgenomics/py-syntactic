"""Capitalize and sentence case functions."""

import re


def capitalize(obj: str | list[str], strict: bool = False) -> list[str]:
    """Capitalize the first letter of each space-delimited word.

    Parameters
    ----------
    obj : str or list of str
        String(s) to capitalize.
    strict : bool
        Lowercase the remaining characters of each word. When ``False``
        (default), only the first letter of each word is touched.

    Returns
    -------
    list of str
        Capitalized string(s).

    Examples
    --------
    >>> capitalize(["fooBar", "HELLO"])
    ['FooBar', 'HELLO']
    >>> capitalize(["fooBar", "HELLO"], strict=True)
    ['Foobar', 'Hello']
    """
    if isinstance(obj, str):
        obj = [obj]
    result = []
    for s in obj:
        if not s:
            result.append(s)
            continue
        words = s.split(" ")
        out_words = []
        for w in words:
            if not w:
                out_words.append(w)
                continue
            first = w[0].upper()
            tail = w[1:].lower() if strict else w[1:]
            out_words.append(first + tail)
        result.append(" ".join(out_words))
    return result


def sentence_case(obj: str | list[str], strict: bool = False) -> list[str]:
    """Convert strings to sentence case.

    Capitalizes the first letter of the first word. Subsequent words are
    lowercased unless they appear to be acronyms (all-caps, mixed case with
    multiple uppercase letters, etc.).

    Parameters
    ----------
    obj : str or list of str
        String(s) to convert.
    strict : bool
        Force ALL words (including the first) to title/lowercase, ignoring
        acronym detection.

    Returns
    -------
    list of str
        Sentence-cased string(s).

    Examples
    --------
    >>> sentence_case(["hello world", "FOO BAR"])
    ['Hello world', 'FOO BAR']
    >>> sentence_case(["hello world", "FOO BAR"], strict=True)
    ['Hello world', 'Foo bar']
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
        result.append(" ".join([first_word, *other_words]))
    return result
