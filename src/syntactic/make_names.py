"""Make syntactically valid names from strings."""

import re
import unicodedata


_GREEK_MAP: dict[str, str] = {
    "\u0391": "Alpha", "\u0392": "Beta", "\u0393": "Gamma",
    "\u0394": "Delta", "\u0395": "Epsilon", "\u0396": "Zeta",
    "\u0397": "Eta", "\u0398": "Theta", "\u0399": "Iota",
    "\u039a": "Kappa", "\u039b": "Lambda", "\u039c": "Mu",
    "\u039d": "Nu", "\u039e": "Xi", "\u039f": "Omicron",
    "\u03a0": "Pi", "\u03a1": "Rho", "\u03a3": "Sigma",
    "\u03a4": "Tau", "\u03a5": "Upsilon", "\u03a6": "Phi",
    "\u03a7": "Chi", "\u03a8": "Psi", "\u03a9": "Omega",
    "\u03b1": "alpha", "\u03b2": "beta", "\u03b3": "gamma",
    "\u03b4": "delta", "\u03b5": "epsilon", "\u03b6": "zeta",
    "\u03b7": "eta", "\u03b8": "theta", "\u03b9": "iota",
    "\u03ba": "kappa", "\u03bb": "lambda", "\u03bc": "mu",
    "\u03bd": "nu", "\u03be": "xi", "\u03bf": "omicron",
    "\u03c0": "pi", "\u03c1": "rho", "\u03c2": "sigma",
    "\u03c3": "sigma", "\u03c4": "tau", "\u03c5": "upsilon",
    "\u03c6": "phi", "\u03c7": "chi", "\u03c8": "psi",
    "\u03c9": "omega",
}


def _transliterate(s: str) -> str:
    """Transliterate unicode characters to ASCII equivalents."""
    s = s.replace("\u00b5", "u")
    s = s.replace("\u03bc", "u")
    s = s.replace("&#181;", "u")
    s = s.replace("\u00e6", "ae")
    s = s.replace("\u00c6", "AE")
    s = s.replace("\u0153", "oe")
    s = s.replace("\u0152", "OE")
    for greek, ascii_name in _GREEK_MAP.items():
        s = s.replace(greek, ascii_name)
    normalized = unicodedata.normalize("NFKD", s)
    result = ""
    for char in normalized:
        if ord(char) < 128:
            result += char
    return result


def _make_names_r(names: list[str], unique: bool = True) -> list[str]:
    """Emulate R's make.names behavior with allow_=TRUE."""
    result = []
    for name in names:
        s = name
        if s and (s[0].isdigit() or s[0] == "."):
            s = "X" + s
        if not s:
            s = "X"
        result.append(s)
    if unique:
        result = _make_unique(result)
    return result


def _make_unique(names: list[str]) -> list[str]:
    """Make a list of names unique by appending numeric suffixes."""
    seen: dict[str, int] = {}
    result = []
    for name in names:
        if name in seen:
            counter = seen[name]
            new_name = f"{name}_{counter}"
            while new_name in seen:
                counter += 1
                new_name = f"{name}_{counter}"
            seen[name] = counter + 1
            seen[new_name] = 1
            result.append(new_name)
        else:
            seen[name] = 1
            result.append(name)
    return result


def make_names(
    obj: list[str] | str,
    unique: bool = True,
    smart: bool = False,
) -> list[str]:
    """Make syntactically valid names out of character vectors.

    Emulates R's syntactic::makeNames() behavior.
    """
    if isinstance(obj, str):
        obj = [obj]
    x = list(obj)
    assert all(len(s) > 0 for s in x), "All strings must be non-empty."
    x = [_transliterate(s) for s in x]
    if smart:
        result = []
        for item in x:
            # Note: apostrophes are NOT stripped here. They get converted to
            # underscores by the [^alnum]->_ regex below, preserving word
            # boundaries (e.g., "5'3' bias" -> "5_3__bias" -> "X5_3_bias").
            s = re.sub(r"&", "_and_", item)
            s = re.sub(r"\+", "_plus_", s)
            s = re.sub(r"\s-\s", " ", s)
            s = re.sub(r"-\s", "_minus_", s)
            s = re.sub(r"^-(.+)$", r"minus_\1", s)
            s = re.sub(r"^(.+)-$", r"\1_minus", s)
            s = re.sub(r"/", "_slash_", s)
            s = re.sub(r"%", "_percent_", s)
            s = s.replace("*", "_times_")
            s = re.sub(r"(\d),(\d)", r"\1\2", s)
            result.append(s)
        x = result
    # Replace all non-alphanumeric characters with underscore.
    x = [re.sub(r"[^a-zA-Z0-9]", "_", s) for s in x]
    # Strip leading/trailing underscores.
    x = [re.sub(r"(^_|_$)", "", s) for s in x]
    # Add X prefix where needed (emulates make.names with allow_=TRUE).
    x = _make_names_r(x, unique=unique)
    # Collapse multiple underscores.
    x = [re.sub(r"_+", "_", s) for s in x]
    # Strip leading/trailing underscores again.
    x = [re.sub(r"(^_|_$)", "", s) for s in x]
    return x
