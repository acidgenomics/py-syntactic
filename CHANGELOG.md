# Changelog

## 0.1.0 (2026-06-19)

### Features

- Add `make_dimnames`: apply `make_names` to row and column name vectors,
  returning a `dict` with `"rownames"` and `"colnames"` keys.
- Add `names` parameter to `kebab_case` for API symmetry (accepted but unused,
  since Python lists have no names attribute).
- Improve feature parity with R `syntactic` v0.8.0 across all case-conversion
  functions.

### Bug Fixes

- Fix `capitalize`: now capitalizes the first letter of **each space-delimited
  word**, matching R's `capitalize()` behaviour.
- Fix `autopad_zeros`: resolve type-checker errors in `pad_zeros.py`; the
  function now correctly type-narrows the scalar vs list input path.

### Changes

- Remove dead `names=` keyword argument from `camel_case`, `upper_camel_case`,
  `snake_case`, `dotted_case`, and `kebab_case`. Python lists have no names
  attribute, so these parameters were always no-ops. This is a **breaking
  change** for callers passing `names=` explicitly.
- Switch license to Apache-2.0.
- Upgrade build backend to `uv_build`.
- Add Sphinx + PyData Theme documentation scaffold with ReadTheDocs config.
- Publish to `python.acidgenomics.com` (private PEP 503 index) instead of
  the git URL installation.
- Update installation instructions in README.

### Tests

- Add `tests/test_make_dimnames.py` (previously untested).
- Expand `test_make_names.py`: add full 14-string R fixture, complex smart
  symbol suite, and uniqueness tests ported from R's `test-makeNames.R`.
- Expand `test_autopad_zeros.py`: add partial-padding error test and 24-element
  mixed-prefix scenario from R's `test-autopadZeros.R`.
- Expand `test_capitalize.py`: add R's canonical 3-string fixture for both
  `capitalize` and `sentence_case`.
- Expand `test_rename.py`: add recursive rename, `camel_case`, `upper_camel_case`,
  `lowercase_ext`, and additional R fixture tests.
- Add `pythonpath = ["src"]` to pytest config so the src-layout package is
  importable without a venv install.

---

## 0.0.1 (2026-02-17)

Initial release.
