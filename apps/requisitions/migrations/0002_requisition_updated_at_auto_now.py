# Generated by Django 3.2.13 on 2022-05-30 12:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('requisitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrequisition',
            name='updated_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='requisition',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
