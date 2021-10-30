# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("wagtailcore", "0016_change_page_url_path_to_text_field")]

    operations = [
        migrations.CreateModel(
            name="SpeakersPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        to="wagtailcore.Page",
                        parent_link=True,
                        serialize=False,
                        primary_key=True,
                        on_delete=models.CASCADE,
                    ),
                ),
                ("api_url", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
