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
            "product": "test_product",
            "campaign_type": "branding",
            "channel": "radio",
            "date": "2022-06-08T00:00:00",
            "conversions": 1.0,
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
            "product": "test_product",
            "campaign_type": "branding",
            "channel": "radio",
            "date": "2022-06-08T00:00:00",
            "conversions": 1.0,
        }
    ]
