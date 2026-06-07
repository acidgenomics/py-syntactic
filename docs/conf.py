"""Sphinx configuration for py-syntactic."""

project = "syntactic"
author = "Michael Steinbaugh"
copyright = "Acid Genomics"  # noqa: A001
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "numpydoc",
]
autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}
napoleon_numpy_docstring = True
napoleon_google_docstring = False
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/acidgenomics/py-syntactic",
    "logo": {"text": "syntactic"},
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
