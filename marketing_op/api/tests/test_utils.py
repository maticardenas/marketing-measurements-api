import pytest
from api.utils import calculate_percentage


# test calculate_percentage with pytest.mark.parametrize


@pytest.mark.parametrize(
    "value, total, expected",
    [
        (10, 100, "10.00"),
        (0, 100, "0.00"),
        (0, 0, "0.00"),
        (10, 0, "0.00"),
        (10, 10, "100.00"),
    ],
)
def test_calculate_percentage(value, total, expected):
    assert calculate_percentage(value, total) == expected
