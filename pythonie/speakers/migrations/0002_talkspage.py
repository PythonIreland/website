# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_auto_20150906_1340'),
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalksPage',
            fields=[
                ('page_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, auto_created=True, to='wagtailcore.Page')),
                ('api_url', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
