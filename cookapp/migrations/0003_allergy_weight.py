# Generated by Django 4.2.5 on 2024-11-21 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookapp', '0002_familyallergy_familymember'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('allergy_id', models.AutoField(db_column='ALLERGY_ID', max_length=11, primary_key=True, serialize=False, verbose_name='アレルギーID')),
                ('material_id', models.IntegerField(db_column='MATERIAL_ID', max_length=11, verbose_name='材料ID')),
                ('allergy_category', models.CharField(db_column='ALLERGY_CATEGORY', max_length=30, verbose_name='アレルギーカテゴリー')),
                ('allergy_name', models.CharField(db_column='ALLERGY_NAME', max_length=30, verbose_name='アレルギー名')),
            ],
            options={
                'db_table': 'allergy',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('weight_id', models.AutoField(db_column='Weight_ID', primary_key=True, serialize=False, verbose_name='体重ID')),
                ('weight', models.FloatField(db_column='Weight', verbose_name='体重')),
                ('register_time', models.DateTimeField(db_column='RegisterTime', verbose_name='登録時間')),
                ('user_id', models.CharField(db_column='User_ID', max_length=50, verbose_name='ユーザID')),
                ('family_id', models.CharField(db_column='Family_ID', max_length=3, verbose_name='家族ID')),
            ],
            options={
                'db_table': 'weight',
                'managed': False,
            },
        ),
    ]