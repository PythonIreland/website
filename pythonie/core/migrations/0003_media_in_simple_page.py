# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.core.fields
import wagtail.core.blocks
import wagtail.images.blocks
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_simplepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.core.fields.StreamField((('heading', wagtail.core.blocks.CharBlock(classname='full title', icon='home')), ('paragraph', wagtail.core.blocks.RichTextBlock(icon='edit')), ('video', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('image', wagtail.images.blocks.ImageChooserBlock(icon='image')), ('slide', wagtail.embeds.blocks.EmbedBlock(icon='media')))),
            preserve_default=True,
        ),
    ]
