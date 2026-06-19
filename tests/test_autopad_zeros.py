"""Tests for autopad_zeros."""

import pytest

from syntactic import autopad_zeros


class TestAutopadZerosInt:
    def test_basic(self) -> None:
        assert autopad_zeros([1, 10, 100]) == ["001", "010", "100"]

    def test_single_digit_unchanged(self) -> None:
        """Single-digit integers: no padding needed (all same width)."""
        assert autopad_zeros([1, 2, 3]) == ["1", "2", "3"]


class TestAutopadZerosStr:
    def test_left_number(self) -> None:
        assert autopad_zeros(["1-EV", "10-EV", "100-EV"]) == [
            "001-EV",
            "010-EV",
            "100-EV",
        ]

    def test_right_number(self) -> None:
        assert autopad_zeros(["A1", "B10", "C100"]) == [
            "A001",
            "B010",
            "C100",
        ]

    def test_no_padding_needed(self) -> None:
        assert autopad_zeros(["A", "B", "C"]) == ["A", "B", "C"]

    def test_partial_padding_raises(self) -> None:
        """Partial match (some numeric, some not) must raise ValueError."""
        with pytest.raises(ValueError, match="Partial padding match detected."):
            autopad_zeros(["1", "10", "X"])

    def test_complex_mixed_prefixes_unchanged(self) -> None:
        """24-element drug-combo vector returns unchanged.

        All strings match the right-side number pattern but the stems differ,
        so no consistent padding width exists.
        Port of R test-autopadZeros.R 'Partial padding' complex scenario.
        """
        obj = [
            "dmso-1",
            "dmso-2",
            "dmso-3",
            "drug1-300nm-1",
            "drug1-300nm-2",
            "drug1-300nm-3",
            "drug1-drug3-1",
            "drug1-drug3-2",
            "drug1-drug3-3",
            "drug2-100nm-1",
            "drug2-100nm-2",
            "drug2-100nm-3",
            "drug2-drug1-1",
            "drug2-drug1-2",
            "drug2-drug1-3",
            "drug2-drug3-1",
            "drug2-drug3-2",
            "drug2-drug3-3",
            "drug3-300nm-1",
            "drug3-300nm-2",
            "drug3-300nm-3",
            "triple-combo-1",
            "triple-combo-2",
            "triple-combo-3",
        ]
        assert autopad_zeros(obj) == obj
