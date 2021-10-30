# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.core.blocks
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_homepage_sponsors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="body",
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            icon="home", classname="full title"
                        ),
                    ),
                    ("paragraph", wagtail.core.blocks.RichTextBlock(icon="edit")),
                    ("video", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    ("slide", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                    ("html", wagtail.core.blocks.RawHTMLBlock(icon="code")),
                )
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="simplepage",
            name="body",
            field=wagtail.core.fields.StreamField(
                (
                    (
                        "heading",
                        wagtail.core.blocks.CharBlock(
                            icon="home", classname="full title"
                        ),
                    ),
                    ("paragraph", wagtail.core.blocks.RichTextBlock(icon="edit")),
                    ("video", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                    ("image", wagtail.images.blocks.ImageChooserBlock(icon="image")),
                    ("slide", wagtail.embeds.blocks.EmbedBlock(icon="media")),
                    ("html", wagtail.core.blocks.RawHTMLBlock(icon="code")),
                )
            ),
            preserve_default=True,
        ),
    ]
