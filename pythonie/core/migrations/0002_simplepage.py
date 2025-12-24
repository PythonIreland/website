# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimplePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        primary_key=True,
                        to="wagtailcore.Page",
                        serialize=False,
                        parent_link=True,
                        auto_created=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        (
                            (
                                "heading",
                                wagtail.blocks.CharBlock(classname="full title"),
                            ),
                            ("paragraph", wagtail.blocks.RichTextBlock()),
                            ("image", wagtail.images.blocks.ImageChooserBlock()),
                        )
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
