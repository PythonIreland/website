# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_auto_20150821_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeakersPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, serialize=False, to='wagtailcore.Page', parent_link=True, auto_created=True)),
                ('api_url', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
