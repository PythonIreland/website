# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0002_restructure_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorshipLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('level', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['level'],
            },
            bases=(models.Model,),
        ),
    ]
