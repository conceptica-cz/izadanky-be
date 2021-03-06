# Generated by Django 3.2.12 on 2022-04-21 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('updates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('external_id', models.IntegerField(blank=True, help_text='UNIS Kód', null=True, unique=True)),
                ('reference_id', models.IntegerField(blank=True, help_text='iČíselník Kód', null=True, unique=True)),
                ('abbreviation', models.CharField(help_text='Zkratka', max_length=10)),
                ('description', models.CharField(db_index=True, help_text='Název', max_length=255)),
                ('is_hospital', models.BooleanField(default=True, help_text='Ambulance')),
                ('is_ambulance', models.BooleanField(default=False, help_text='Lůžkové oddělení')),
                ('image', models.ImageField(blank=True, help_text='Obrázek', null=True, upload_to='clinics')),
            ],
            options={
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('external_id', models.IntegerField(blank=True, help_text='UNIS Kód', null=True, unique=True)),
                ('abbreviation', models.CharField(help_text='Zkratka', max_length=10)),
                ('description', models.CharField(help_text='Název', max_length=255)),
                ('specialization_code', models.CharField(blank=True, help_text='Odbornost (kód)', max_length=3)),
                ('icp', models.CharField(help_text='IČP', max_length=8)),
                ('ns', models.CharField(blank=True, help_text='Nákladove středisko', max_length=6)),
                ('workplace_code', models.CharField(blank=True, help_text='Zkrácený kód pracoviště dle ÚZIS', max_length=10)),
                ('for_insurance', models.BooleanField(blank=True, help_text='Používat pro vykazování pojištění', null=True, unique=True)),
            ],
            options={
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalClinic',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('external_id', models.IntegerField(blank=True, db_index=True, help_text='UNIS Kód', null=True)),
                ('reference_id', models.IntegerField(blank=True, db_index=True, help_text='iČíselník Kód', null=True)),
                ('abbreviation', models.CharField(help_text='Zkratka', max_length=10)),
                ('description', models.CharField(db_index=True, help_text='Název', max_length=255)),
                ('is_hospital', models.BooleanField(default=True, help_text='Ambulance')),
                ('is_ambulance', models.BooleanField(default=False, help_text='Lůžkové oddělení')),
                ('image', models.TextField(blank=True, help_text='Obrázek', max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical clinic',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDepartment',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('external_id', models.IntegerField(blank=True, db_index=True, help_text='UNIS Kód', null=True)),
                ('abbreviation', models.CharField(help_text='Zkratka', max_length=10)),
                ('description', models.CharField(help_text='Název', max_length=255)),
                ('specialization_code', models.CharField(blank=True, help_text='Odbornost (kód)', max_length=3)),
                ('icp', models.CharField(help_text='IČP', max_length=8)),
                ('ns', models.CharField(blank=True, help_text='Nákladove středisko', max_length=6)),
                ('workplace_code', models.CharField(blank=True, help_text='Zkrácený kód pracoviště dle ÚZIS', max_length=10)),
                ('for_insurance', models.BooleanField(blank=True, db_index=True, help_text='Používat pro vykazování pojištění', null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical department',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalPerson',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('person_number', models.CharField(db_index=True, help_text='Osobní číslo', max_length=100)),
                ('name', models.CharField(help_text='Jméno', max_length=255)),
                ('f_title', models.CharField(default='', help_text='Titul před', max_length=100)),
                ('l_title', models.CharField(default='', help_text='Titul za', max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical person',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('person_number', models.CharField(help_text='Osobní číslo', max_length=100, unique=True)),
                ('name', models.CharField(help_text='Jméno', max_length=255)),
                ('f_title', models.CharField(default='', help_text='Titul před', max_length=100)),
                ('l_title', models.CharField(default='', help_text='Titul za', max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['name'], name='references__name_5f7174_idx'),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.person'),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalperson',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='clinic',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Klinika', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='references.clinic'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.department'),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicaldepartment',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.clinic'),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalclinic',
            name='update',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='updates.update'),
        ),
        migrations.AddField(
            model_name='department',
            name='clinic',
            field=models.ForeignKey(blank=True, help_text='Klinika', null=True, on_delete=django.db.models.deletion.CASCADE, to='references.clinic'),
        ),
        migrations.AddIndex(
            model_name='clinic',
            index=models.Index(fields=['description'], name='references__descrip_4ee902_idx'),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['description'], name='references__descrip_30cdc7_idx'),
        ),
    ]
