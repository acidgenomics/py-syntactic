"""Case conversion functions."""

import re

from syntactic._engine import _syntactic


def _camel_case(
    x: list[str],
    format: str = "lower",
    strict: bool = True,
    **kwargs: bool,
) -> list[str]:
    """Internal camelCase conversion engine."""
    assert format in ("lower", "upper")
    x = _syntactic(x, **kwargs)
    x = [s.replace("_", ".") for s in x]
    if strict:
        x = [s.lower() for s in x]
    result = []
    for item in x:
        if format == "lower":
            s = re.sub(r"^(\w+)\b", lambda m: m.group(1).lower(), item)
        elif format == "upper":
            s = re.sub(r"^([a-z])", lambda m: m.group(1).upper(), item)
        else:
            s = item
        s = re.sub(r"([a-zA-Z])\.([0-9])", r"\1\2", s)
        s = re.sub(r"\.([a-zA-Z])", lambda m: m.group(1).upper(), s)
        if "." in s:
            replacement = "x" if format == "lower" else "X"
            s = s.replace(".", replacement)
        result.append(s)
    return result


def camel_case(
    obj: str | list[str],
    strict: bool = True,
    smart: bool = True,
    prefix: bool = True,
) -> list[str]:
    """Convert strings to lowerCamelCase.

    Parameters
    ----------
    obj : str or list of str
        String(s) to convert.
    strict : bool
        Enforce strict name sanitization. When ``True``, this does not allow
        the return of any capitalized acronyms; e.g. "RNA" becomes "Rna".
    smart : bool
        Handle complicated special cases, such as mixed case acronyms,
        plus/minus, and percentages.
    prefix : bool
        Prepend an "x" character if the string begins with a syntactically
        invalid character, such as a number.

    Returns
    -------
    list of str
        Strings converted to lowerCamelCase.

    Examples
    --------
    >>> camel_case(["human genomeVersion", "sampleID"])
    ['humanGenomeVersion', 'sampleId']
    >>> camel_case(["sampleID"], strict=False)
    ['sampleID']
    """
    if isinstance(obj, str):
        obj = [obj]
    return _camel_case(x=list(obj), format="lower", strict=strict, smart=smart, prefix=prefix)


def upper_camel_case(
    obj: str | list[str],
    strict: bool = True,
    smart: bool = True,
    prefix: bool = True,
) -> list[str]:
    """Convert strings to UpperCamelCase (PascalCase).

    Parameters
    ----------
    obj : str or list of str
        String(s) to convert.
    strict : bool
        Enforce strict name sanitization. When ``True``, this does not allow
        the return of any capitalized acronyms; e.g. "RNA" becomes "Rna".
    smart : bool
        Handle complicated special cases, such as mixed case acronyms,
        plus/minus, and percentages.
    prefix : bool
        Prepend an "X" character if the string begins with a syntactically
        invalid character, such as a number.

    Returns
    -------
    list of str
        UpperCamelCase string(s).

    Examples
    --------
    >>> upper_camel_case(["human_genome_version", "sample_id"])
    ['HumanGenomeVersion', 'SampleId']
    """
    if isinstance(obj, str):
        obj = [obj]
    return _camel_case(x=list(obj), format="upper", strict=strict, smart=smart, prefix=prefix)


def _snake_case(x: list[str], **kwargs: bool) -> list[str]:
    """Internal snake_case conversion engine."""
    x = _syntactic(x, **kwargs)
    return [s.lower() for s in x]


def snake_case(
    obj: str | list[str],
    smart: bool = True,
    prefix: bool = True,
) -> list[str]:
    """Convert strings to snake_case.

    Parameters
    ----------
    obj : str or list of str
        String(s) to convert.
    smart : bool
        Handle complicated special cases, such as mixed case acronyms,
        plus/minus, and percentages.
    prefix : bool
        Prepend an "x" character if the string begins with a syntactically
        invalid character, such as a number.

    Returns
    -------
    list of str
        Strings converted to snake_case.

    Examples
    --------
    >>> snake_case(["human genomeVersion", "sampleID"])
    ['human_genome_version', 'sample_id']
    """
    if isinstance(obj, str):
        obj = [obj]
    return _snake_case(x=list(obj), smart=smart, prefix=prefix)


def dotted_case(
    obj: str | list[str],
    smart: bool = True,
    prefix: bool = True,
) -> list[str]:
    """Convert strings to dotted.case.

    Parameters
    ----------
    obj : str or list of str
        String(s) to convert.
    smart : bool
        Handle complicated special cases, such as mixed case acronyms,
        plus/minus, and percentages.
    prefix : bool
        Prepend an "x" character if the string begins with a syntactically
        invalid character, such as a number.

    Returns
    -------
    list of str
        Strings converted to dotted.case.

    Examples
    --------
    >>> dotted_case(["human genomeVersion", "sampleID"])
    ['human.genome.version', 'sample.id']
    """
    if isinstance(obj, str):
        obj = [obj]
    x = _snake_case(x=list(obj), smart=smart, prefix=prefix)
    return [s.replace("_", ".") for s in x]


def kebab_case(
    obj: str | list[str],
    smart: bool = True,
    prefix: bool = True,
) -> list[str]:
    """Convert strings to kebab-case.

    Parameters
    ----------
    obj : str or list of str
        String(s) to convert.
    smart : bool
        Handle complicated special cases, such as mixed case acronyms,
        plus/minus, and percentages.
    prefix : bool
        Prepend an "x" character if the string begins with a syntactically
        invalid character, such as a number.

    Returns
    -------
    list of str
        Strings converted to kebab-case.

    Examples
    --------
    >>> kebab_case(["human genomeVersion", "sampleID"])
    ['human-genome-version', 'sample-id']
    """
    if isinstance(obj, str):
        obj = [obj]
    x = snake_case(obj, smart=smart, prefix=prefix)
    return [s.replace("_", "-") for s in x]
