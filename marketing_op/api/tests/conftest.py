import pytest
from core.models import Product, Campaign, CampaignType, Conversion, Channel


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def product():
    return Product.objects.create(name="test_product")


@pytest.fixture
def campaign(product: Product) -> Campaign:
    return Campaign.objects.create(
        name="test_campaign",
        product=product,
        campaign_type=CampaignType.objects.get(name="branding"),
    )


@pytest.fixture
def conversion(campaign: Campaign):
    return Conversion.objects.create(
        campaign=Campaign.objects.get(name="test_campaign"),
        channel=Channel.objects.get(name="radio"),
        date="2022-06-08",
        conversions=1.0,
    )
