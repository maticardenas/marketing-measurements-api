from http import HTTPStatus

import pytest
from ninja.testing import TestClient

from api.tests.factories import ConversionFactory, ChannelFactory
from core.models import Conversion


def test_channel_sales_percentage(client: TestClient, token_auth_headers: dict):
    # given
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
        date="2021-01-01",
        conversions=120.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
        date="2021-02-01",
        conversions=80.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="tv"),
        date="2021-02-01",
        conversions=420.00,
    )

    # when
    response = client.get(
        "/stats/channel-sales-percentages/", headers=token_auth_headers
    )

    # then
    assert response.json() == {
        "data": [
            {"channel": "tv", "percentage": "67.74"},
            {"channel": "radio", "percentage": "32.26"},
        ]
    }


def test_channel_sales_percentage_filtered(
    client: TestClient, token_auth_headers: dict
):
    # given
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
        date="2021-01-01",
        conversions=120.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
        date="2021-02-01",
        conversions=80.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="tv"),
        date="2021-02-01",
        conversions=420.00,
    )
    query = "?channels=radio"

    # when
    response = client.get(
        f"/stats/channel-sales-percentages/{query}", headers=token_auth_headers
    )

    # then
    assert response.json() == {
        "data": [
            {"channel": "radio", "percentage": "32.26"},
        ]
    }


def test_get_channel_weekly_sales(client: TestClient, token_auth_headers: dict):
    # given
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
        date="2024-01-01",
        conversions=120.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
        date="2024-01-01",
        conversions=220.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="tv"),
        date="2024-01-01",
        conversions=420.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="facebook"),
        date="2024-01-15",
        conversions=245.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="instagram"),
        date="2024-01-15",
        conversions=555.00,
    )

    # when
    response = client.get("/stats/channel-weekly-sales/", headers=token_auth_headers)

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [
            {"channel": "radio", "year": 2024, "week": 1, "sales": 340.0},
            {"channel": "tv", "year": 2024, "week": 1, "sales": 420.0},
            {"channel": "facebook", "year": 2024, "week": 3, "sales": 245.0},
            {"channel": "instagram", "year": 2024, "week": 3, "sales": 555.0},
        ]
    }


def test_get_weekly_sales_pagination(
    client: TestClient, token_auth_headers: dict, multiple_conversions: list[Conversion]
):
    # given
    query = "?page_size=2"

    # when
    response = client.get(
        f"/stats/channel-weekly-sales/{query}", headers=token_auth_headers
    )

    # then
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["data"]) == 2


def test_get_weekly_sales_pagination_more_than_max(
    client: TestClient, token_auth_headers: dict, multiple_conversions: list[Conversion]
):
    # given
    query = "?page_size=200"

    # when
    response = client.get(
        f"/stats/channel-weekly-sales/{query}", headers=token_auth_headers
    )

    # then
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "less_than_equal",
                "loc": ["query", "page_size"],
                "msg": "Input should be less than or equal to 100",
                "ctx": {"le": 100},
            }
        ]
    }


@pytest.mark.parametrize(
    "offset, page_size",
    [
        (1, -1),
        (-1, 1),
        (-1, -1),
        (11, 101),
    ],
)
def test_get_weekly_sales_pagination_negative(
    offset,
    page_size,
    client: TestClient,
    token_auth_headers: dict,
    multiple_conversions: list[Conversion],
):
    # given
    query = f"?offset={offset}&page_size={page_size}"

    # when
    response = client.get(
        f"/stats/channel-weekly-sales/{query}", headers=token_auth_headers
    )

    # then
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
