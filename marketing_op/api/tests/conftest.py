import pytest

from api.tests.factories import (
    ConversionFactory,
    ProductFactory,
    CampaignTypeFactory,
    CampaignFactory,
    ChannelFactory,
)
from core.models import Product, Campaign, CampaignType, Conversion


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


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
