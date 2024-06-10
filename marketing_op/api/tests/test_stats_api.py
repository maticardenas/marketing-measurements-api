from ninja.testing import TestClient

from api.tests.factories import ConversionFactory, ChannelFactory


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
        "stats/channel-sales-percentages/", headers=token_auth_headers
    )

    # then
    assert response.json() == {
        "data": [
            {"channel": "tv", "percentage": "67.74"},
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
    response = client.get("stats/channel-weekly-sales/", headers=token_auth_headers)

    # then
    assert response.json() == {
        "data": [
            {"channel": "radio", "year": 2024, "week": 1, "sales": 340.0},
            {"channel": "tv", "year": 2024, "week": 1, "sales": 420.0},
            {"channel": "facebook", "year": 2024, "week": 3, "sales": 245.0},
            {"channel": "instagram", "year": 2024, "week": 3, "sales": 555.0},
        ]
    }
