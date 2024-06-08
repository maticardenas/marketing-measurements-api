import factory

from core.constants import CHANNELS, CAMPAIGN_TYPES
from core.models import Conversion, Channel, Product, Campaign, CampaignType


class ChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Channel

    name = factory.Iterator([channel[0] for channel in CHANNELS])


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("pystr", max_chars=15)


class CampaignTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CampaignType

    name = factory.Iterator([campaign_type[0] for campaign_type in CAMPAIGN_TYPES])


class CampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Campaign

    name = factory.Faker("pystr", max_chars=15)
    product = factory.SubFactory(ProductFactory)
    campaign_type = factory.Iterator(CampaignType.objects.all())


class ConversionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Conversion

    campaign = factory.SubFactory(CampaignFactory)
    channel = factory.Iterator(Channel.objects.all())
    date = factory.Faker("date")
    conversions = factory.Faker("pyfloat", min_value=0, max_value=10000)
