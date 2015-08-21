# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_auto_20150812_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeakersPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, primary_key=True, parent_link=True, serialize=False, to='wagtailcore.Page')),
                ('api_url', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
