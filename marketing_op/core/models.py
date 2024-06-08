from django.db import models

from core.constants import CAMPAIGN_TYPES, CHANNELS


class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CampaignType(models.Model):
    name = models.CharField(max_length=50, choices=CAMPAIGN_TYPES, unique=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=255, choices=CHANNELS, unique=True)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    campaign_type = models.ForeignKey(CampaignType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Conversion(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    date = models.DateField()
    conversions = models.FloatField()

    def __str__(self):
        return f"{self.campaign.name} - {self.channel.name} - {self.date}"
