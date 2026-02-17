"""Internal engine functions for syntactic name processing."""

import re

from syntactic.make_names import make_names


def _sanitize_acronyms(x: list[str]) -> list[str]:
    """Sanitize mixed-case acronyms in strings."""
    result = []
    for item in x:
        # Work with dots as word separators for regex matching.
        s = item.replace("_", ".")
        # Identifier variants (e.g. "Id" to "ID").
        s = re.sub(r"\b(id)\b", "ID", s, flags=re.IGNORECASE)
        # Molarity (e.g. "10nM" to "10nm").
        s = re.sub(
            r"\b([mnu]M)\b",
            lambda m: m.group(1).lower(),
            s,
        )
        # Also handle digit-prefixed molarity (e.g. "X10uM" -> "X10um").
        s = re.sub(
            r"([0-9]+[mnu]M)\b",
            lambda m: m.group(1).lower(),
            s,
        )
        # Pluralized acronyms (e.g. "UMIs" to "UMIS").
        s = re.sub(
            r"\b([A-Z0-9]+)s\b",
            lambda m: m.group(1) + "S",
            s,
        )
        # Mixed case RNA types.
        s = re.sub(
            r"\b((?:mi|nc|pi|r)RNA)\b",
            lambda m: m.group(1).upper(),
            s,
        )
        # RNA interference.
        s = re.sub(r"\b(RNAi)\b", "RNAI", s)
        # Ethanol.
        s = re.sub(r"\b(EtOH)\b", "Etoh", s)
        # Convert back to underscores.
        s = s.replace(".", "_")
        result.append(s)
    return result


def _syntactic(
    x: list[str],
    smart: bool = True,
    prefix: bool = True,
) -> list[str]:
    """Core syntactic name processing engine."""
    x = make_names(x, smart=smart, unique=False)
    if smart:
        # Strip any remaining apostrophes after make_names.
        x = [s.replace("'", "") for s in x]
        # Standardize any mixed case acronyms.
        x = _sanitize_acronyms(x)
    # Include "X" prefix by default, but allow manual disable.
    if not prefix:
        x = [re.sub(r"^X([^a-zA-Z])", r"\1", s, flags=re.IGNORECASE) for s in x]
    result = []
    for item in x:
        # Establish word boundaries for camelCase acronyms.
        # Acronym following a word: e.g. "nCount" -> "n_Count"
        s = re.sub(r"([a-z])([A-Z])", r"\1_\2", item)
        # Word following an acronym: e.g. "HTMLRemap" -> "HTML_Remap"
        s = re.sub(r"([A-Z0-9])([A-Z])([a-z]{2,})", r"\1_\2\3", s)
        # Handle remaining long acronym sequences.
        s = re.sub(
            r"([A-Z0-9]{2,})([A-Z])([a-z]).+",
            lambda m: m.group(1) + "_" + m.group(2) + m.group(3),
            s,
        )
        result.append(s)
    return result
