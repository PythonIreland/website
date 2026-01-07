# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0004_auto_20150726_1412"),
        ("core", "0005_auto_20150726_1416"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePageSponsorRelationship",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        primary_key=True,
                        auto_created=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "homepage",
                    models.ForeignKey(to="core.HomePage", on_delete=models.CASCADE),
                ),
                (
                    "level",
                    models.ForeignKey(
                        to="sponsors.SponsorshipLevel", on_delete=models.CASCADE
                    ),
                ),
                (
                    "sponsor",
                    models.ForeignKey(to="sponsors.Sponsor", on_delete=models.CASCADE),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
