# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_simplepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='full title', icon='home')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock(icon='edit')), ('video', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock(icon='image')), ('slide', wagtail.wagtailembeds.blocks.EmbedBlock(icon='media')))),
            preserve_default=True,
        ),
    ]
