# Generated by Django 3.1 on 2020-03-16 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("secrets_api", "0002_auto_20200316_1812"),
    ]

    operations = [
        migrations.AddField(
            model_name="secret",
            name="DEBUG",
            field=models.CharField(default="True", max_length=200),
        ),
    ]
