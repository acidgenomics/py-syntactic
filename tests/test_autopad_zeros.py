"""Tests for autopad_zeros."""

from syntactic import autopad_zeros


class TestAutopadZerosInt:
    def test_basic(self) -> None:
        assert autopad_zeros([1, 10, 100]) == ["001", "010", "100"]


class TestAutopadZerosStr:
    def test_left_number(self) -> None:
        assert autopad_zeros(["1-EF", "10-EF", "100-EF"]) == [
            "001-EF",
            "010-EF",
            "100-EF",
        ]

    def test_right_number(self) -> None:
        assert autopad_zeros(["EF-1", "EF-10", "EF-100"]) == [
            "EF-001",
            "EF-010",
            "EF-100",
        ]

    def test_no_padding_needed(self) -> None:
        assert autopad_zeros(["a", "b", "c"]) == ["a", "b", "c"]
