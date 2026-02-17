"""Tests for dotted.case conversion."""

from syntactic import dotted_case

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


class TestDottedCase:
    def test_unnamed(self) -> None:
        assert dotted_case(UNNAMED) == [
            "percent.gc",
            "x10um",
            "x5.3.bias",
            "x5prime",
            "g2m.score",
            "hello.world",
            "hello.world",
            "mazda.rx4",
            "n.count",
            "rnai.clones",
            "tx2gene",
            "tx2.gene.id",
            "worfdb.html.remap",
            "x123",
        ]

    def test_x_handling_prefix_mode(self) -> None:
        assert dotted_case(
            ["Xenobiotic", "xenobiotic", "XX123", "X123", "xx123", "x123", "123"],
            prefix=False,
        ) == ["xenobiotic", "xenobiotic", "xx123", "123", "xx123", "123", "123"]

    def test_ampersand_smart(self) -> None:
        assert dotted_case(["here&there"], smart=True) == ["here.and.there"]
        assert dotted_case(["here&there"], smart=False) == ["here.there"]

    def test_accented_characters(self) -> None:
        obj = ["bi\u00e8re", "encyclop\u00e6dia", "\u00e9tude", "qu\u00e9 tal"]
        assert dotted_case(obj, smart=True) == [
            "biere",
            "encyclopaedia",
            "etude",
            "que.tal",
        ]
