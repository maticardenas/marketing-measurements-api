import base64

import pytest
from ninja.testing import TestClient
from openapi_tester import SchemaTester
from openapi_tester.clients import OpenAPINinjaClient

from api.marketing_op_api import router, auth_router
from api.services.auth import generate_token
from api.tests.factories import (
    ConversionFactory,
    ProductFactory,
    CampaignTypeFactory,
    CampaignFactory,
    ChannelFactory,
)
from core.models import Product, Campaign, CampaignType, Conversion
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def oas_path():
    return CURRENT_DIR.parent / "design" / "openapi.yaml"


@pytest.fixture
def product() -> Product:
    product = ProductFactory()
    return product


@pytest.fixture
def campaign_type() -> CampaignType:
    campaign_type = CampaignTypeFactory()
    return campaign_type


@pytest.fixture
def campaign() -> Campaign:
    campaign = CampaignFactory()
    return campaign


@pytest.fixture
def conversion() -> Conversion:
    conversions = ConversionFactory(
        channel=ChannelFactory(name="radio"),
    )
    return conversions


@pytest.fixture
def multiple_conversions() -> list[Conversion]:
    multiple_conversions = ConversionFactory.create_batch(10)
    return multiple_conversions


@pytest.fixture
def client(oas_path: Path):
    schema_tester = SchemaTester(schema_file_path=str(oas_path))
    return OpenAPINinjaClient(
        router_or_app=router,
        schema_tester=schema_tester,
        path_prefix="/api/marketing",
    )


@pytest.fixture
def auth_client(oas_path: Path) -> TestClient:
    schema_tester = SchemaTester(schema_file_path=str(oas_path))
    return OpenAPINinjaClient(
        router_or_app=auth_router,
        schema_tester=schema_tester,
        path_prefix="/api/auth",
    )


@pytest.fixture
def auth_headers():
    username = "marketing_op"
    password = "marketing_op_supersecret"
    encoded_creds = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode(
        "utf-8"
    )
    return {"Authorization": f"Basic {encoded_creds}"}


@pytest.fixture
def token():
    return generate_token("marketing_op")


@pytest.fixture()
def token_auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}
