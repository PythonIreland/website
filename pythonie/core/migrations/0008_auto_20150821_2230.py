# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_homepage_sponsors"),
    ]

    operations = [
        migrations.AlterField(
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
                    ("html", wagtail.blocks.RawHTMLBlock(icon="code")),
                )
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="simplepage",
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
                    ("html", wagtail.blocks.RawHTMLBlock(icon="code")),
                )
            ),
            preserve_default=True,
        ),
    ]
