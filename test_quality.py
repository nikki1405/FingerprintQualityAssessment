import pytest

from quality_assessment import normalize


def test_normalize_clamps_and_scales_values_between_zero_and_one():
    assert normalize(5, 0, 10) == 0.5
    assert normalize(-1, 0, 10) == 0.0
    assert normalize(12, 0, 10) == 1.0
