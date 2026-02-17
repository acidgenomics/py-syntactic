"""Syntactic: Make syntactically valid names out of character vectors.

A Python port of the R syntactic package by Acid Genomics.
"""

from syntactic.capitalize import capitalize, sentence_case
from syntactic.case_conversion import (
    camel_case,
    dotted_case,
    kebab_case,
    snake_case,
    upper_camel_case,
)
from syntactic.make_names import make_names
from syntactic.make_words import make_label, make_title, make_words
from syntactic.pad_zeros import autopad_zeros
from syntactic.rename import syntactic_rename

__all__ = [
    "autopad_zeros",
    "camel_case",
    "capitalize",
    "dotted_case",
    "kebab_case",
    "make_label",
    "make_names",
    "make_title",
    "make_words",
    "sentence_case",
    "snake_case",
    "syntactic_rename",
    "upper_camel_case",
]

__version__ = "0.7.2"
