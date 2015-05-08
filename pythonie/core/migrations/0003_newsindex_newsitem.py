# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import wagtailnews.models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0013_update_golive_expire_help_text'),
        ('core', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsIndex',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, primary_key=True, to='wagtailcore.Page')),
            ],
            options={
            },
            bases=(wagtailnews.models.NewsIndexMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Published date', default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('body', wagtail.wagtailcore.fields.RichTextField()),
                ('newsindex', models.ForeignKey(to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
                'ordering': ('-date',),
            },
            bases=(models.Model,),
        ),
    ]
