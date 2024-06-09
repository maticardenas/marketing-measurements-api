from http import HTTPStatus

import pytest

from api.marketing_measurements import router
from core.models import Conversion
from ninja.testing import TestClient


@pytest.fixture
def client():
    return TestClient(router)


def test_get_marketing_data(client: TestClient, conversion: Conversion):
    # given - when
    response = client.get("/")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "product": conversion.campaign.product.name,
            "campaign": conversion.campaign.name,
            "campaign_type": conversion.campaign.campaign_type.name,
            "channel": conversion.channel.name,
            "date": conversion.date,
            "conversions": conversion.conversions,
        }
    ]


def test_get_marketing_data_no_data(client: TestClient, conversion: Conversion):
    # given
    query = "?channels=tv"

    # when
    response = client.get(f"/{query}")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_marketing_data_multiple_values_same_property(
    client: TestClient, conversion: Conversion
):
    # given
    query = "?channels=tv&channels=radio"

    # when
    response = client.get(f"/{query}")

    # then
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "product": conversion.campaign.product.name,
            "campaign": conversion.campaign.name,
            "campaign_type": conversion.campaign.campaign_type.name,
            "channel": conversion.channel.name,
            "date": conversion.date,
            "conversions": conversion.conversions,
        }
    ]


def test_get_multiple_conversions(
    client: TestClient, multiple_conversions: list[Conversion]
):
    # given - when
    response = client.get("/")

    # then
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 10
