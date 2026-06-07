"""Apply make_names to row and column name vectors."""

from syntactic.make_names import make_names


def make_dimnames(
    rownames: list[str] | None = None,
    colnames: list[str] | None = None,
) -> dict[str, list[str] | None]:
    """Apply syntactic naming to row and/or column name vectors.

    Equivalent to R's ``makeDimnames``: applies :func:`make_names` with
    ``unique=True`` to each supplied name vector.

    Parameters
    ----------
    rownames : list[str] or None
        Row names to sanitize. Returned unchanged (as ``None``) when not
        provided.
    colnames : list[str] or None
        Column names to sanitize. Returned unchanged (as ``None``) when not
        provided.

    Returns
    -------
    dict
        Mapping with keys ``"rownames"`` and ``"colnames"``, each either a
        sanitized list or ``None``.

    Examples
    --------
    >>> make_dimnames(rownames=["Row 1", "Row 2"], colnames=["My Col"])
    {'rownames': ['row_1', 'row_2'], 'colnames': ['my_col']}
    >>> make_dimnames(colnames=["Bad Name!", "Good"])
    {'rownames': None, 'colnames': ['bad_name', 'good']}
    """
    return {
        "rownames": make_names(rownames, unique=True) if rownames is not None else None,
        "colnames": make_names(colnames, unique=True) if colnames is not None else None,
    }
