# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_media_in_simple_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(icon='home', classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='edit')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('slide', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media'))), default=None),
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
