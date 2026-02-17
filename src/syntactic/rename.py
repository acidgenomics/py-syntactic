"""Rename files and directories using syntactic naming functions."""

import os
import platform
import tempfile
from collections.abc import Callable
from pathlib import Path

from syntactic.case_conversion import (
    camel_case,
    kebab_case,
    snake_case,
    upper_camel_case,
)


def _is_case_sensitive_fs(path: str = ".") -> bool:
    """Check if the file system is case-sensitive."""
    try:
        with tempfile.NamedTemporaryFile(dir=path, prefix="TmP_", delete=False) as tmp:
            tmp_path = tmp.name
        upper_path = tmp_path.upper()
        lower_path = tmp_path.lower()
        is_sensitive = not (os.path.exists(upper_path) and os.path.exists(lower_path))
        os.unlink(tmp_path)
        return is_sensitive
    except OSError, PermissionError:
        return platform.system() == "Linux"


def _get_file_depth(path: str) -> int:
    """Get the depth of a file path."""
    return len(Path(path).parts)


def _get_recursive_paths(
    paths: list[str],
) -> tuple[list[str], list[str]]:
    """Get all recursive file and directory paths."""
    all_paths: set[str] = set()
    for raw_path in paths:
        real_path = os.path.realpath(raw_path)
        all_paths.add(real_path)
        if os.path.isdir(real_path):
            for root, dirnames, filenames in os.walk(real_path):
                for d in dirnames:
                    all_paths.add(os.path.realpath(os.path.join(root, d)))
                for f in filenames:
                    all_paths.add(os.path.realpath(os.path.join(root, f)))
    dirs = sorted(
        [p for p in all_paths if os.path.isdir(p)],
        key=_get_file_depth,
        reverse=True,
    )
    files = sorted(
        [p for p in all_paths if not os.path.isdir(p)],
        key=_get_file_depth,
        reverse=True,
    )
    return files, dirs


def _file_ext(path: str) -> str | None:
    """Get the file extension, handling compound extensions."""
    name = os.path.basename(path)
    compound_exts = [".fastq.gz", ".tar.gz", ".tar.bz2", ".tar.xz"]
    for ext in compound_exts:
        if name.endswith(ext):
            return ext.lstrip(".")
    _, ext = os.path.splitext(name)
    return ext.lstrip(".") if ext else None


def _basename_sans_ext(path: str) -> str:
    """Get the basename without its extension."""
    name = os.path.basename(path)
    compound_exts = [".fastq.gz", ".tar.gz", ".tar.bz2", ".tar.xz"]
    for ext in compound_exts:
        if name.endswith(ext):
            return name[: -len(ext)]
    stem, _ = os.path.splitext(name)
    return stem


def _get_naming_function(fun: str) -> Callable[..., list[str]]:
    """Validate and return the naming function."""
    valid_funs: dict[str, Callable[..., list[str]]] = {
        "kebab_case": kebab_case,
        "snake_case": snake_case,
        "camel_case": camel_case,
        "upper_camel_case": upper_camel_case,
    }
    if fun not in valid_funs:
        raise ValueError(
            f"Invalid function '{fun}'. Must be one of: {', '.join(valid_funs.keys())}"
        )
    return valid_funs[fun]


def _resolve_from_paths(
    path: list[str],
    recursive: bool,
) -> list[str]:
    """Resolve input paths to a list of source paths for renaming."""
    for p in path:
        if not os.path.exists(p):
            raise FileNotFoundError(f"Path not found: {p}")
    if len(path) == 1 and os.path.isdir(path[0]) and not recursive:
        dirpath = os.path.realpath(path[0])
        entries = os.listdir(dirpath)
        return [os.path.join(dirpath, e) for e in entries]
    if recursive:
        files, dirs = _get_recursive_paths(path)
        return files + dirs
    return [os.path.realpath(p) for p in path]


def _compute_to_path(
    from_path: str,
    naming_fn: Callable[..., list[str]],
    quiet: bool,
) -> str:
    """Compute the target path for a single source path."""
    dirname = os.path.dirname(from_path)
    if os.path.isdir(from_path):
        stem = os.path.basename(from_path)
        ext = None
    else:
        stem = _basename_sans_ext(from_path)
        ext = _file_ext(from_path)
    if not stem or not stem[0].isalnum():
        if not quiet:
            print(f"Skipping {from_path}")
        return from_path
    result = naming_fn(stem, smart=True, prefix=False)
    new_stem = result[0] if isinstance(result, list) else result
    basename = f"{new_stem}.{ext}" if ext else new_stem
    return os.path.join(dirname, basename)


def _execute_renames(
    from_paths: list[str],
    to_paths: list[str],
    case_sensitive: bool,
    quiet: bool,
) -> None:
    """Execute file rename operations."""
    for from_path, to_path in zip(from_paths, to_paths, strict=False):
        if from_path == to_path:
            continue
        if not quiet:
            print(f"Renaming {from_path} to {to_path}")
        if case_sensitive:
            os.rename(from_path, to_path)
        else:
            tmp_path = os.path.join(
                os.path.dirname(from_path),
                f".tmp.{os.path.basename(from_path)}",
            )
            os.rename(from_path, tmp_path)
            os.rename(tmp_path, to_path)


def syntactic_rename(
    path: str | list[str],
    recursive: bool = False,
    fun: str = "kebab_case",
    quiet: bool = False,
    dry_run: bool = False,
) -> dict[str, list[str]]:
    """Rename files and/or directories using a syntactic naming function.

    Args:
        path: A file path, directory path, or list of paths. When a single
            directory is given, its contents are renamed.
        recursive: If True, recurse into directories.
        fun: Naming function to use.
        quiet: Suppress output messages.
        dry_run: Preview changes without renaming.
    """
    naming_fn = _get_naming_function(fun)
    if isinstance(path, str):
        path = [path]
    from_paths = _resolve_from_paths(path, recursive)
    case_sensitive = _is_case_sensitive_fs(os.path.dirname(from_paths[0]) if from_paths else ".")
    to_paths = [_compute_to_path(fp, naming_fn, quiet) for fp in from_paths]
    if dry_run:
        for f, t in zip(from_paths, to_paths, strict=False):
            if not quiet:
                print(f"[dry-run] {f} -> {t}")
        return {"from": [], "to": []}
    _execute_renames(from_paths, to_paths, case_sensitive, quiet)
    return {"from": from_paths, "to": to_paths}
