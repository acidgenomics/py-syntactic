"""Tests for UpperCamelCase conversion."""

from syntactic import upper_camel_case

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


class TestUpperCamelCaseStrict:
    def test_unnamed(self) -> None:
        assert upper_camel_case(UNNAMED, strict=True) == [
            "PercentGc",
            "X10um",
            "X5X3Bias",
            "X5prime",
            "G2mScore",
            "HelloWorld",
            "HelloWorld",
            "MazdaRx4",
            "NCount",
            "RnaiClones",
            "Tx2gene",
            "Tx2GeneId",
            "WorfdbHtmlRemap",
            "X123",
        ]


class TestUpperCamelCaseNonStrict:
    def test_unnamed(self) -> None:
        assert upper_camel_case(UNNAMED, strict=False) == [
            "PercentGC",
            "X10um",
            "X5X3Bias",
            "X5prime",
            "G2MScore",
            "HelloWorld",
            "HELLOWORLD",
            "MazdaRX4",
            "NCount",
            "RNAIClones",
            "Tx2gene",
            "TX2GeneID",
            "WorfdbHTMLRemap",
            "X123",
        ]


class TestUpperCamelCasePrefix:
    def test_disable_x_prefix(self) -> None:
        assert upper_camel_case(["1 foo bar"]) == ["X1FooBar"]
        assert upper_camel_case(["1 foo bar"], prefix=False) == ["1FooBar"]
