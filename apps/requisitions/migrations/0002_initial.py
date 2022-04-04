# Generated by Django 3.2.12 on 2022-04-04 16:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('requisitions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrequisition',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalrequisition',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
    ]
