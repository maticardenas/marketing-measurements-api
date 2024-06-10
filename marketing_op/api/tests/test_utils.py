import pytest
from django.db.models import Q

from api.utils import calculate_percentage, build_filters_query


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


def test_build_filters_query():
    # given
    products = ["product1", "product2"]
    campaign_types = ["always on", "performance"]
    channels = ["facebook", "instagram"]
    campaigns = ["campaign1", "campaign2"]
    start_date = "2021-01-01"
    end_date = "2021-02-01"

    # when
    query = build_filters_query(
        products=products,
        campaign_types=campaign_types,
        channels=channels,
        campaigns=campaigns,
        start_date=start_date,
        end_date=end_date,
    )

    # then
    assert query == (
        Q(product__name__in=products)
        & Q(campaign__campaign_type__name__in=campaign_types)
        & Q(channel__name__in=channels)
        & Q(campaign__name__in=campaigns)
        & Q(date__gte=start_date)
        & Q(date__lte=end_date)
    )
