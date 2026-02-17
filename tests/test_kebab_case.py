"""Tests for kebab-case conversion."""

from syntactic import kebab_case

UNNAMED = [
    "%GC",
    "10uM",
    "5'3' bias",
    "5prime",
    "G2M.Score",
    "hello world",
    "HELLO WORLD",
    "Mazda RX4",
    "nCount",
    "RNAi clones",
    "tx2gene",
    "TX2GeneID",
    "worfdbHTMLRemap",
    "x123",
]


class TestKebabCase:
    def test_unnamed(self) -> None:
        assert kebab_case(UNNAMED) == [
            "percent-gc",
            "x10um",
            "x5-3-bias",
            "x5prime",
            "g2m-score",
            "hello-world",
            "hello-world",
            "mazda-rx4",
            "n-count",
            "rnai-clones",
            "tx2gene",
            "tx2-gene-id",
            "worfdb-html-remap",
            "x123",
        ]

    def test_disable_x_prefix(self) -> None:
        assert kebab_case(["1 foo bar"]) == ["x1-foo-bar"]
        assert kebab_case(["1 foo bar"], prefix=False) == ["1-foo-bar"]
