"""Tests for capitalize and sentence_case."""

from syntactic import capitalize, sentence_case

# Canonical R test fixture (test-capitalize.R and test-sentenceCase.R).
R_FIXTURE = [
    "the quick Brown fox",
    "using AIC for model selection",
    "NASA",
]


class TestCapitalizeNonStrict:
    def test_basic(self) -> None:
        assert capitalize(["fooBar", "HELLO"]) == ["FooBar", "HELLO"]

    def test_r_fixture(self) -> None:
        """Port of R test-capitalize.R: strict=FALSE."""
        assert capitalize(R_FIXTURE, strict=False) == [
            "The Quick Brown Fox",
            "Using AIC For Model Selection",
            "NASA",
        ]


class TestCapitalizeStrict:
    def test_basic(self) -> None:
        assert capitalize(["fooBar", "HELLO"], strict=True) == ["Foobar", "Hello"]

    def test_r_fixture(self) -> None:
        """Port of R test-capitalize.R: strict=TRUE lowercases non-first letters."""
        assert capitalize(R_FIXTURE, strict=True) == [
            "The Quick Brown Fox",
            "Using Aic For Model Selection",
            "Nasa",
        ]


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

    def test_r_fixture(self) -> None:
        """Port of R test-sentenceCase.R: capitalize first word, preserve acronyms."""
        assert sentence_case(R_FIXTURE) == [
            "The quick brown fox",
            "Using AIC for model selection",
            "NASA",
        ]
