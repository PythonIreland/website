import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meetups", "0003_remove_meetup_announced"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meetup",
            name="updated",
            field=models.DateTimeField(
                default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.UTC)
            ),
            preserve_default=True,
        ),
    ]
