# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.images.blocks
import wagtail.core.fields
import wagtail.core.blocks


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
                    wagtail.core.fields.StreamField(
                        (
                            (
                                "heading",
                                wagtail.core.blocks.CharBlock(classname="full title"),
                            ),
                            ("paragraph", wagtail.core.blocks.RichTextBlock()),
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
