"""Tests for make_words, make_title, make_label."""

from syntactic import make_label, make_title, make_words

MW = [
    "log10GenesPerUMI",
    "mitoVsCoding",
    "words already",
    "NASA",
    "nGene",
]


class TestMakeWords:
    def test_mw(self) -> None:
        assert make_words(MW) == [
            "log10 genes per UMI",
            "mito vs. coding",
            "words already",
            "NASA",
            "n gene",
        ]


class TestMakeTitle:
    def test_mw(self) -> None:
        assert make_title(MW) == [
            "Log10 genes per UMI",
            "Mito vs. coding",
            "Words already",
            "NASA",
            "N gene",
        ]


class TestMakeLabel:
    def test_mw(self) -> None:
        assert make_label(MW) == [
            "Log10 genes per UMI",
            "Mito vs. coding",
            "Words already",
            "NASA",
            "N gene",
        ]
