# Generated by Django 5.0.6 on 2024-06-08 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CampaignType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("branding", "BRANDING"),
                            ("performance", "PERFORMANCE"),
                            ("always on", "ALWAYS ON"),
                        ],
                        max_length=50,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("tv", "TV"),
                            ("radio", "RADIO"),
                            ("ooh", "OOH"),
                            ("facebook", "FACEBOOK"),
                            ("print", "PRINT"),
                            ("tiktok", "TIKTOK"),
                            ("instagram", "INSTAGRAM"),
                            ("db360 - prospecting", "DB360"),
                            ("db360 - retargeting", "DB360 - RETARGETING"),
                            ("google - branded search", "GOOGLE - BRANDED SEARCH"),
                            (
                                "google - non-branded search",
                                "GOOGLE - NON-BRANDED SEARCH",
                            ),
                        ],
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "campaign_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.campaigntype",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.product"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Conversion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("conversions", models.FloatField()),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.campaign"
                    ),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.channel"
                    ),
                ),
            ],
        ),
    ]
