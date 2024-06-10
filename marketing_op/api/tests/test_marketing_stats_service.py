from api.services.marketing_stats import (
    get_channel_sales_percentages,
    get_channel_weekly_sales,
)
from api.tests.factories import ChannelFactory, ConversionFactory


def test_get_channel_sales_percentages():
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
    channel_sales_percentages = get_channel_sales_percentages(
        filters={"channels": ["radio"]},
    )

    # then
    assert channel_sales_percentages == [{"channel": "radio", "percentage": "32.26"}]


def test_get_channel_sales_percentages_multiple_channels():
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
    ConversionFactory(
        channel=ChannelFactory(name="facebook"),
        date="2021-02-01",
        conversions=245.00,
    )
    ConversionFactory(
        channel=ChannelFactory(name="instagram"),
        date="2021-02-01",
        conversions=555.00,
    )

    # when
    channel_sales_percentages = get_channel_sales_percentages(
        filters={"channels": ["radio", "tv", "facebook", "instagram"]},
    )

    # then
    assert channel_sales_percentages == [
        {"channel": "instagram", "percentage": "39.08"},
        {"channel": "tv", "percentage": "29.58"},
        {"channel": "facebook", "percentage": "17.25"},
        {"channel": "radio", "percentage": "14.08"},
    ]


def test_get_channel_weekly_sales():
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
    channel_weekly_sales = get_channel_weekly_sales(
        filters={"channels": ["radio", "tv", "facebook", "instagram"]},
    )

    # then
    assert channel_weekly_sales == [
        {"year": 2024, "week": 1, "channel": "radio", "sales": 340.0},
        {"year": 2024, "week": 1, "channel": "tv", "sales": 420.0},
        {"year": 2024, "week": 3, "channel": "facebook", "sales": 245.0},
        {"year": 2024, "week": 3, "channel": "instagram", "sales": 555.0},
    ]
