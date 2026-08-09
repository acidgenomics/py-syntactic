"""Make human-readable words, labels, and titles from variable names."""

import re

from syntactic._engine import _syntactic
from syntactic.capitalize import sentence_case


def make_words(obj: str | list[str]) -> list[str]:
    """Convert variable names to human-readable word strings.

    Strings that already contain spaces are returned unmodified.

    Parameters
    ----------
    obj : str or list of str
        Variable name(s) to convert.

    Returns
    -------
    list of str
        Human-readable word string(s).

    Examples
    --------
    >>> make_words(["nGene", "log10GenesPerUMI"])
    ['n gene', 'log10 genes per UMI']
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

    Applies :func:`make_words` then :func:`~syntactic.capitalize.sentence_case`
    to each string.

    Parameters
    ----------
    obj : str or list of str
        Variable name(s) to convert.

    Returns
    -------
    list of str
        Title-cased string(s).

    Examples
    --------
    >>> make_title(["nGene", "log10GenesPerUMI"])
    ['N gene', 'Log10 genes per UMI']
    """
    if isinstance(obj, str):
        obj = [obj]
    words_list = make_words(obj)
    return sentence_case(words_list)


def make_label(obj: str | list[str]) -> list[str]:
    """Convert variable names to human-readable labels.

    Applies :func:`make_words` and capitalizes the first letter of the result.

    Parameters
    ----------
    obj : str or list of str
        Variable name(s) to convert.

    Returns
    -------
    list of str
        Human-readable label(s).

    Examples
    --------
    >>> make_label(["nGene", "log10GenesPerUMI"])
    ['N gene', 'Log10 genes per UMI']
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
