# Generated by Django 3.2.12 on 2022-04-04 16:28

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='HistoricalTag',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical tag',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='references__name_1a56d8_idx'),
        ),
        migrations.AddField(
            model_name='historicaltag',
            name='history_relation',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='history', to='references.tag'),
        ),
    ]
