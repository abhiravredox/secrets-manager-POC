# Generated by Django 3.1 on 2020-03-16 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("secrets_api", "0003_secret_debug"),
    ]

    operations = [
        migrations.RenameField(model_name="secret", old_name="NAME", new_name="name",),
    ]
