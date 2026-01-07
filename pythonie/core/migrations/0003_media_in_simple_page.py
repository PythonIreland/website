# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_simplepage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="simplepage",
            name="body",
            field=wagtail.fields.StreamField(
                (
                    (
                        "heading",
                        wagtail.blocks.CharBlock(classname="full title", icon="home"),
                    ),
                    ("paragraph", wagtail.blocks.RichTextBlock(icon="edit")),
                    ("video", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    ("slide", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                )
            ),
            preserve_default=True,
        ),
    ]
