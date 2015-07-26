# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150708_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='show_sponsors',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepage',
            name='show_sponsors',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
