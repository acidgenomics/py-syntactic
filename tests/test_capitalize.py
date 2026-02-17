"""Tests for capitalize and sentence_case."""

from syntactic import capitalize, sentence_case


class TestCapitalizeNonStrict:
    def test_basic(self) -> None:
        assert capitalize(["fooBar", "HELLO"]) == ["FooBar", "HELLO"]


class TestCapitalizeStrict:
    def test_basic(self) -> None:
        assert capitalize(["fooBar", "HELLO"], strict=True) == ["Foobar", "Hello"]


class TestSentenceCase:
    def test_basic(self) -> None:
        assert sentence_case(["hello world", "FOO BAR"]) == [
            "Hello world",
            "FOO BAR",
        ]

    def test_strict(self) -> None:
        assert sentence_case(["hello world", "FOO BAR"], strict=True) == [
            "Hello world",
            "Foo bar",
        ]

    def test_acronym_preservation(self) -> None:
        """Acronyms (all-caps words) preserved in non-strict mode."""
        assert sentence_case(["using AIC for model selection"]) == [
            "Using AIC for model selection",
        ]
