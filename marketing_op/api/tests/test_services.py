from datetime import datetime

from api.services.marketing import get_marketing_data
from core.models import Conversion


def test_get_marketing_data(conversion: Conversion):
    # given - when
    marketing_data = get_marketing_data()

    # then
    assert len(marketing_data) == 1
    assert marketing_data[0]["campaign"] == "test_campaign"
    assert marketing_data[0]["channel"] == "radio"
    assert datetime.strftime(marketing_data[0]["date"], "%Y-%m-%d") == "2022-06-08"
    assert marketing_data[0]["conversions"] == 1.0


def test_get_marketing_data_not_found(conversion: Conversion):
    # given - when
    marketing_data = get_marketing_data(channels=["tv"])

    # then
    assert len(marketing_data) == 0


def test_get_marketing_data_multiple_values_same_property(conversion: Conversion):
    # given - when
    marketing_data = get_marketing_data(channels=["tv", "radio"])

    # then
    assert len(marketing_data) == 1
    assert marketing_data[0]["campaign"] == "test_campaign"
    assert marketing_data[0]["channel"] == "radio"
    assert datetime.strftime(marketing_data[0]["date"], "%Y-%m-%d") == "2022-06-08"
    assert marketing_data[0]["conversions"] == 1.0
