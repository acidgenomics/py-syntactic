"""Tests for make_dimnames."""

from syntactic import make_dimnames


class TestMakeDimnames:
    def test_r_matrix_equivalent(self) -> None:
        """Port of R test-makeDimnames.R: duplicate row/col names are made unique."""
        result = make_dimnames(
            rownames=["1-a", "1-a"],
            colnames=["2-b", "2-b"],
        )
        assert result["rownames"] == ["X1_a", "X1_a_1"]
        assert result["colnames"] == ["X2_b", "X2_b_1"]

    def test_rownames_only(self) -> None:
        result = make_dimnames(rownames=["Row 1", "Row 2"])
        assert result["rownames"] == ["Row_1", "Row_2"]
        assert result["colnames"] is None

    def test_colnames_only(self) -> None:
        result = make_dimnames(colnames=["Bad Name!", "Good"])
        assert result["rownames"] is None
        assert result["colnames"] == ["Bad_Name", "Good"]

    def test_none_when_not_provided(self) -> None:
        result = make_dimnames()
        assert result["rownames"] is None
        assert result["colnames"] is None
