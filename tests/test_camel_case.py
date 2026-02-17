"""Tests for camelCase conversion."""

from syntactic import camel_case

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


class TestCamelCaseStrict:
    def test_unnamed(self) -> None:
        assert camel_case(UNNAMED, strict=True) == [
            "percentGc",
            "x10um",
            "x5x3Bias",
            "x5prime",
            "g2mScore",
            "helloWorld",
            "helloWorld",
            "mazdaRx4",
            "nCount",
            "rnaiClones",
            "tx2gene",
            "tx2GeneId",
            "worfdbHtmlRemap",
            "x123",
        ]

    def test_acronyms_strict(self) -> None:
        assert camel_case(
            ["cliUpdateRPackages", "externalIDs", "externalRNAs"],
            strict=True,
        ) == ["cliUpdateRPackages", "externalIds", "externalRnas"]


class TestCamelCaseNonStrict:
    def test_unnamed(self) -> None:
        assert camel_case(UNNAMED, strict=False) == [
            "percentGC",
            "x10um",
            "x5x3Bias",
            "x5prime",
            "g2mScore",
            "helloWorld",
            "helloWORLD",
            "mazdaRX4",
            "nCount",
            "rnaiClones",
            "tx2gene",
            "tx2GeneID",
            "worfdbHTMLRemap",
            "x123",
        ]


class TestCamelCaseDelimitedNumbers:
    def test_delimited_numbers(self) -> None:
        dn = ["1,000,000", "0.01", "2018-01-01", "res.0.1"]
        assert camel_case(dn) == ["x1000000", "x0x01", "x2018x01x01", "res0x1"]


class TestCamelCasePlusMinus:
    def test_plus_minus(self) -> None:
        pm = ["100%", "+/-", "a +/- b", "dox-", "dox+", "-dox", "+dox", "/", "-"]
        assert camel_case(pm) == [
            "x100Percent",
            "plusSlashMinus",
            "aPlusSlashMinusB",
            "doxMinus",
            "doxPlus",
            "minusDox",
            "plusDox",
            "slash",
            "x",
        ]


class TestCamelCasePrefix:
    def test_disable_x_prefix(self) -> None:
        assert camel_case(["1 foo bar"]) == ["x1FooBar"]
        assert camel_case(["1 foo bar"], prefix=False) == ["1FooBar"]

    def test_x_handling_prefix_mode(self) -> None:
        assert camel_case(
            ["Xenobiotic", "xenobiotic", "XX123", "X123", "xx123", "x123", "123"],
            prefix=False,
        ) == ["xenobiotic", "xenobiotic", "xx123", "123", "xx123", "123", "123"]
