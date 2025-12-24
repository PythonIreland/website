# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_media_in_simple_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                (
                    (
                        "heading",
                        wagtail.blocks.CharBlock(icon="home", classname="full title"),
                    ),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="edit")),
                    ("video", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    ("slide", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                ),
                default=None,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="homepage",
            name="show_meetups",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="simplepage",
            name="show_meetups",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
