# Generated by Django 2.0.1 on 2018-01-05 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geography', '0004_auto_20180105_0201'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Geography',
            new_name='Geometry',
        ),
    ]