# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_homepage_sponsors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(icon='home', classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='edit')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('slide', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code')))),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(icon='home', classname='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='edit')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('slide', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='code')))),
            preserve_default=True,
        ),
    ]
