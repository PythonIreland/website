# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("meetups", "0003_remove_meetup_announced"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meetup",
            name="updated",
            field=models.DateTimeField(
                default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc)
            ),
            preserve_default=True,
        ),
    ]
