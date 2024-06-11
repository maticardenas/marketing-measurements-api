from http import HTTPStatus

from django.http import HttpResponse
from ninja.testing import TestClient
from pytest_bdd import scenario, given, then, when

from api.tests.factories import ConversionFactory, ChannelFactory


@scenario(
    "marketing_measurements.feature",
    "Retrieve marketing measurements for specific channel",
)
def test_marketing_measurements():
    pass


@given("a set of existing conversions for marketing campaigns")
def a_set_of_existing_conversions_for_marketing_campaigns():
    ConversionFactory(
        channel=ChannelFactory(name="radio"),
    )
    ConversionFactory(
        channel=ChannelFactory(name="tv"),
    )
    ConversionFactory(
        channel=ChannelFactory(name="facebook"),
    )


@when(
    "requesting marketing measurements through API for a specific channel",
    target_fixture="response",
)
def requesting_marketing_measurements_through_api_for_a_specific_channel(
    client: TestClient, token_auth_headers: dict
):
    query = "?channels=facebook"
    response = client.get(
        f"/measurements/{query}",
        headers=token_auth_headers,
    )
    return response


@then("I should receive a list of measurements for that channel")
def the_api_should_return_the_marketing_measurements_for_the_specific_channel(
    response: HttpResponse,
):
    assert response.status_code == HTTPStatus.OK
    response_body = response.json()

    assert len(response_body["data"]) == 1
    assert response_body["data"][0]["channel"] == "facebook"
