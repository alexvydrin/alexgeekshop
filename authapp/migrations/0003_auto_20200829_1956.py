# Generated by Django 3.0.8 on 2020-08-29 16:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20200828_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 31, 16, 56, 28, 548832, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(default=18, verbose_name='возраст'),
        ),
    ]
