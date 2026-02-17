"""Autopad zeros for consistent string sorting."""

import re


def autopad_zeros(obj: int | str | list[int] | list[str]) -> list[str]:
    """Automatically pad numbers with leading zeros for consistent sorting."""
    if isinstance(obj, (int, str)):
        obj = [obj]
    if all(isinstance(v, int) for v in obj):
        strs = [str(v) for v in obj]
        return autopad_zeros(strs)
    x = [str(v) for v in obj]

    int_pattern = r"^([0-9]+)$"
    left_pattern = r"^([0-9]+)(.+)$"
    right_pattern = r"^(.*[^0-9]+)([0-9]+)$"

    is_int = all(re.match(int_pattern, s) for s in x)
    is_left = all(re.match(left_pattern, s) for s in x)
    is_right = all(re.match(right_pattern, s) for s in x)

    if is_int:
        width = max(len(s) for s in x)
        return [s.zfill(width) for s in x]
    elif is_left and not is_int:
        matches = [re.match(left_pattern, s) for s in x]
        nums = [m.group(1) for m in matches]
        stems = [m.group(2) for m in matches]
        width = max(len(n) for n in nums)
        padded = [n.zfill(width) for n in nums]
        return [p + s for p, s in zip(padded, stems, strict=False)]
    elif is_right:
        matches = [re.match(right_pattern, s) for s in x]
        stems = [m.group(1) for m in matches]
        nums = [m.group(2) for m in matches]
        width = max(len(n) for n in nums)
        padded = [n.zfill(width) for n in nums]
        return [s + p for s, p in zip(stems, padded, strict=False)]
    else:
        has_int = any(re.match(int_pattern, s) for s in x)
        has_left = any(re.match(left_pattern, s) for s in x)
        has_right = any(re.match(right_pattern, s) for s in x)
        if has_int or has_left or has_right:
            raise ValueError("Partial padding match detected.")
        return list(x)
