# Generated by Django 4.2.5 on 2024-11-18 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familyallergy',
            fields=[
                ('family_allergy_id', models.AutoField(db_column='FamilyAllergyID', primary_key=True, serialize=False, verbose_name='家族アレルギーID')),
                ('allerg_id', models.CharField(db_column='Allergy_ID', max_length=3, verbose_name='アレルギーID')),
                ('family_id', models.CharField(db_column='Family_ID', max_length=50, verbose_name='家族ID')),
            ],
            options={
                'db_table': 'familyallergy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Familymember',
            fields=[
                ('family_id', models.AutoField(db_column='Family_ID', primary_key=True, serialize=False, verbose_name='家族ID')),
                ('family_name', models.CharField(db_column='Family_Name', max_length=20, verbose_name='名前')),
                ('family_age', models.CharField(db_column='Family_Age', max_length=3, verbose_name='年齢')),
                ('family_gender', models.CharField(db_column='Family_Gender', max_length=3, verbose_name='性別')),
                ('family_height', models.FloatField(db_column='Family_height', verbose_name='身長')),
                ('family_weight', models.FloatField(db_column='Family_weight', verbose_name='体重')),
            ],
            options={
                'db_table': 'familymember',
                'managed': False,
            },
        ),
    ]
