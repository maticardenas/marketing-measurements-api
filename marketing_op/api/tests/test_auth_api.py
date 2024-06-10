import uuid
from http import HTTPStatus
from ninja.testing import TestClient


def test_get_token(auth_client: TestClient, auth_headers: dict):
    # given - when
    response = auth_client.get("/token/", headers=auth_headers)

    # then
    assert response.status_code == HTTPStatus.OK
    assert uuid.UUID(response.json()["data"]["token"], version=4)


def test_get_token_unauthorized(auth_client: TestClient):
    # given - when
    response = auth_client.get("/token/")

    # then
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token_invalid_credentials(auth_client: TestClient):
    # given
    auth_headers = {"Authorization": "Basic dGVzdDp0ZXN0"}

    # when
    response = auth_client.get("/token/", headers=auth_headers)

    # then
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_token_validity(
    client: TestClient, auth_client: TestClient, auth_headers: dict
):
    # given
    response = auth_client.get("/token/", headers=auth_headers)

    assert response.status_code == HTTPStatus.OK

    token = response.json()["data"]["token"]

    # when
    response = client.get(
        "/measurements/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
