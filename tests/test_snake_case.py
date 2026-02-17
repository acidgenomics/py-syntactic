"""Tests for snake_case conversion."""

from syntactic import snake_case

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

PM = ["100%", "+/-", "a +/- b", "dox-", "dox+", "-dox", "+dox", "/", "-"]


class TestSnakeCase:
    def test_unnamed(self) -> None:
        assert snake_case(UNNAMED) == [
            "percent_gc",
            "x10um",
            "x5_3_bias",
            "x5prime",
            "g2m_score",
            "hello_world",
            "hello_world",
            "mazda_rx4",
            "n_count",
            "rnai_clones",
            "tx2gene",
            "tx2_gene_id",
            "worfdb_html_remap",
            "x123",
        ]

    def test_acronyms(self) -> None:
        assert snake_case(["cliUpdateRPackages", "externalIDs", "externalRNAs"]) == [
            "cli_update_r_packages",
            "external_ids",
            "external_rnas",
        ]

    def test_plus_minus(self) -> None:
        assert snake_case(PM) == [
            "x100_percent",
            "plus_slash_minus",
            "a_plus_slash_minus_b",
            "dox_minus",
            "dox_plus",
            "minus_dox",
            "plus_dox",
            "slash",
            "x",
        ]
