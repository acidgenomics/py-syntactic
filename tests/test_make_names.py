"""Tests for make_names."""

from syntactic import make_names

# Canonical 14-string fixture (same as R's AcidTest syntactic[["character"]]).
# Note: last element is "123" (pure digits); case-conversion tests use "x123"
# because .syntactic("123") → makeNames → "X123" → lowercase → "x123".
UNNAMED = [
    "%GC",
    "10uM",
    "5'-3' bias",
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
    "123",
]


class TestMakeNames:
    def test_basic(self) -> None:
        assert make_names(["hello world", "foo bar"]) == ["hello_world", "foo_bar"]

    def test_unnamed_fixture(self) -> None:
        """Port of R test-makeNames.R: makeNames on the canonical 14-string vector."""
        assert make_names(UNNAMED) == [
            "GC",
            "X10uM",
            "X5_3_bias",
            "X5prime",
            "G2M_Score",
            "hello_world",
            "HELLO_WORLD",
            "Mazda_RX4",
            "nCount",
            "RNAi_clones",
            "tx2gene",
            "TX2GeneID",
            "worfdbHTMLRemap",
            "X123",
        ]

    def test_unique_duplicates(self) -> None:
        assert make_names(["a-b", "a-b"], unique=True) == ["a_b", "a_b_1"]
        assert make_names(["a-b", "a-b"], unique=False) == ["a_b", "a_b"]

    def test_unique_numeric_strings(self) -> None:
        """Duplicate numeric strings get X-prefix before uniquification."""
        assert make_names(["1", "1"], unique=True) == ["X1", "X1_1"]

    def test_unique(self) -> None:
        assert make_names(["a", "a", "b"], unique=True) == ["a", "a_1", "b"]

    def test_numeric_prefix(self) -> None:
        assert make_names(["1foo", "2bar"]) == ["X1foo", "X2bar"]

    def test_smart_symbols(self) -> None:
        assert make_names(["%GC", "a+b"], smart=True) == [
            "percent_GC",
            "a_plus_b",
        ]
        assert make_names(["%GC", "a+b"], smart=False) == ["GC", "a_b"]

    def test_smart_full_suite(self) -> None:
        """Port of R test-makeNames.R: 9-element smart symbol test.

        Note: R strips apostrophes in smart mode (giving "ab" for "a'b"),
        whereas Python converts apostrophes to "_" (giving "a_b") because
        _syntactic() strips them post-hoc at the case-conversion layer.
        The Python behaviour is intentional to preserve word boundaries in
        strings like "5'-3' bias" → "X5_3_bias".
        """
        assert make_names(
            [
                "a - b",
                "a- b",
                "a -b",
                "a+b",
                "a/b",
                "a&b",
                "a'b",
                "a,b",
                "1,0",
            ],
            unique=False,
            smart=True,
        ) == [
            "a_b",
            "a_minus_b",
            "a_b",
            "a_plus_b",
            "a_slash_b",
            "a_and_b",
            "a_b",  # Python: apostrophe → "_"; R: apostrophe stripped → "ab"
            "a_b",
            "X10",
        ]

    def test_apostrophe_preserves_boundary(self) -> None:
        """Apostrophes become underscores, preserving word boundaries."""
        assert make_names(["5'-3' bias"], smart=False) == ["X5_3_bias"]

    def test_latin1_special_chars(self) -> None:
        """Nordic and special Latin-1 chars not handled by NFKD normalization."""
        assert make_names(["Ø"]) == ["O"]
        assert make_names(["ø"]) == ["o"]
        assert make_names(["Ð"]) == ["D"]
        assert make_names(["ð"]) == ["d"]
        assert make_names(["Þ"]) == ["TH"]
        assert make_names(["þ"]) == ["th"]
        assert make_names(["ß"]) == ["ss"]
        assert make_names(["×"], smart=False) == ["X"]
        assert make_names(["÷"], smart=False) == ["X"]
        assert make_names(["×"], smart=True) == ["times"]
        assert make_names(["÷"], smart=True) == ["slash"]

    def test_greek_characters(self) -> None:
        assert make_names(["alpha", "Beta", "γ", "Δ", "ε"]) == [
            "alpha",
            "Beta",
            "gamma",
            "Delta",
            "epsilon",
        ]
        assert make_names(["α", "β", "γ"]) == ["alpha", "beta", "gamma"]
        assert make_names(["Δ", "Ε", "Ω"]) == ["Delta", "Epsilon", "Omega"]
        assert make_names(["αβγ"]) == ["alphabetagamma"]

    def test_smart_times(self) -> None:
        assert make_names(["a*b"], smart=True) == ["a_times_b"]
        assert make_names(["a*b"], smart=False) == ["a_b"]
