# Generated by Django"s makemigrations command
import csv

from django.db import migrations
from pathlib import Path
import logging

CURRENT_DIR = Path(__file__).resolve().parent
CSV_DIR = CURRENT_DIR.parent / "data" / "demo_data.csv"


def dump_demo_data_in_db(apps, schema_editor):
    """
    Creates demo data provided in CSV file.
    """
    logging.info("Dumping demo data from CSV file in the database.")

    CampaignType = apps.get_model("core", "CampaignType")
    Channel = apps.get_model("core", "Channel")
    Product = apps.get_model("core", "Product")
    Campaign = apps.get_model("core", "Campaign")
    Conversion = apps.get_model("core", "Conversion")

    # Read and insert data from CSV file
    with CSV_DIR.open() as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_name = row["product"]
            campaign_type_name = row["campaign_type"]
            channel_name = row["channel"]
            campaign_name = row["campaign"]
            date = row["date"]
            conversions = row["conversions"]

            product, created = Product.objects.get_or_create(name=product_name)

            campaign_type, created = CampaignType.objects.get_or_create(
                name=campaign_type_name
            )

            channel, created = Channel.objects.get_or_create(name=channel_name)

            campaign, created = Campaign.objects.get_or_create(
                name=campaign_name, campaign_type=campaign_type, product=product
            )

            Conversion.objects.create(
                campaign=campaign, channel=channel, date=date, conversions=conversions
            )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_auto_20240608_1755"),
    ]

    operations = [
        migrations.RunPython(dump_demo_data_in_db),
    ]
