# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtailnews.models
import modelcluster.fields
import django.utils.timezone
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0013_update_golive_expire_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, serialize=False, to='wagtailcore.Page', primary_key=True, parent_link=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('homepage', modelcluster.fields.ParentalKey(to='core.HomePage', related_name='homepage_segments')),
            ],
            options={
                'verbose_name': 'Homepage Segment',
                'verbose_name_plural': 'Homepage Segments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsIndex',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, serialize=False, to='wagtailcore.Page', primary_key=True, parent_link=True)),
            ],
            options={
            },
            bases=(wagtailnews.models.NewsIndexMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Published date')),
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
        migrations.CreateModel(
            name='PageSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('body', wagtail.wagtailcore.fields.RichTextField()),
                ('location', models.CharField(default='main', max_length=5, choices=[('main', 'Main section'), ('right', 'Right side'), ('left', 'Left side')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='homepagesegment',
            name='segment',
            field=models.ForeignKey(to='core.PageSegment', related_name='homepage_segments'),
            preserve_default=True,
        ),
    ]
