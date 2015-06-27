# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='status',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='visibility',
        ),
        migrations.AddField(
            model_name='sponsor',
            name='url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
