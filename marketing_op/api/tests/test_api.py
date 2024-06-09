from http import HTTPStatus

import pytest

from api.marketing_op_api import router
from api.tests.factories import ConversionFactory, CampaignFactory
from core.models import Conversion
from ninja.testing import TestClient


@pytest.fixture
def client():
    return TestClient(router)


def test_get_marketing_data(client: TestClient, conversion: Conversion):
    # given - when
    response = client.get("/measurements/")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [
            {
                "product": conversion.campaign.product.name,
                "campaign": conversion.campaign.name,
                "campaign_type": conversion.campaign.campaign_type.name,
                "channel": conversion.channel.name,
                "date": conversion.date,
                "conversions": conversion.conversions,
            }
        ]
    }


def test_get_marketing_data_no_data(client: TestClient, conversion: Conversion):
    # given
    query = "?channels=tv"

    # when
    response = client.get(f"/measurements/{query}")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": []}


def test_get_marketing_data_multiple_values_same_property(
    client: TestClient, conversion: Conversion
):
    # given
    query = "?channels=tv&channels=radio"

    # when
    response = client.get(f"/measurements/{query}")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "data": [
            {
                "product": conversion.campaign.product.name,
                "campaign": conversion.campaign.name,
                "campaign_type": conversion.campaign.campaign_type.name,
                "channel": conversion.channel.name,
                "date": conversion.date,
                "conversions": conversion.conversions,
            }
        ]
    }


def test_get_multiple_conversions(
    client: TestClient, multiple_conversions: list[Conversion]
):
    # given - when
    response = client.get("/measurements/")

    # then
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["data"]) == 10


def test_get_conversions_filter_by_date(client: TestClient):
    # given
    ConversionFactory(
        campaign=CampaignFactory(name="earlier_campaign"),
        date="2021-01-01",
    )
    ConversionFactory(
        campaign=CampaignFactory(name="later_campaign"),
        date="2023-02-01",
    )
    query = "?start_date=2021-01-01&end_date=2022-01-31"

    # when - then
    response = client.get(f"/measurements/{query}")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()["data"][0]["campaign"] == "earlier_campaign"
    assert response.json()["data"][0]["date"] == "2021-01-01"

    query = "?start_date=2023-01-01"

    response = client.get(f"/measurements/{query}")

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()["data"][0]["campaign"] == "later_campaign"
    assert response.json()["data"][0]["date"] == "2023-02-01"
