# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import wagtail.wagtailcore.fields
import wagtailnews.models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0013_update_golive_expire_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, to='wagtailcore.Page', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageSegment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('homepage', modelcluster.fields.ParentalKey(related_name='homepage_segments', to='core.HomePage')),
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
                ('page_ptr', models.OneToOneField(parent_link=True, to='wagtailcore.Page', auto_created=True, serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(wagtailnews.models.NewsIndexMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('body', wagtail.wagtailcore.fields.RichTextField()),
                ('location', models.CharField(default='main', choices=[('main', 'Main section'), ('right', 'Right side'), ('left', 'Left side')], max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='homepagesegment',
            name='segment',
            field=models.ForeignKey(related_name='homepage_segments', to='core.PageSegment'),
            preserve_default=True,
        ),
    ]
