"""Tests for make_names."""

from syntactic import make_names


class TestMakeNames:
    def test_basic(self) -> None:
        assert make_names(["hello world", "foo bar"]) == ["hello_world", "foo_bar"]

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

    def test_apostrophe_preserves_boundary(self) -> None:
        """Apostrophes become underscores, preserving word boundaries."""
        assert make_names(["5'3' bias"], smart=False) == ["X5_3_bias"]

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
        assert make_names(["α", "β", "γ"]) == ["alpha", "beta", "gamma"]
        assert make_names(["Δ", "Ε", "Ω"]) == ["Delta", "Epsilon", "Omega"]
        assert make_names(["αβγ"]) == ["alphabetagamma"]

    def test_smart_times(self) -> None:
        assert make_names(["a*b"], smart=True) == ["a_times_b"]
        assert make_names(["a*b"], smart=False) == ["a_b"]
