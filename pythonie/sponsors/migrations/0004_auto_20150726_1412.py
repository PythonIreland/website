from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("sponsors", "0003_sponsorshiplevel"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sponsorshiplevel",
            options={"ordering": ["-level"]},
        ),
    ]
