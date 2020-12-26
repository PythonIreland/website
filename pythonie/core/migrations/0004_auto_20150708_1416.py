# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_media_in_simple_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(icon='home', classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='edit')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('slide', wagtail.embeds.blocks.EmbedBlock(icon='media'))), default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='show_meetups',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepage',
            name='show_meetups',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
