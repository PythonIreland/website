# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meetups", "0004_auto_20150705_1641"),
    ]

    operations = [
        migrations.DeleteModel(
            name="MeetupUpdate",
        ),
    ]
