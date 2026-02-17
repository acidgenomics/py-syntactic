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
