# Generated by Django 4.2.5 on 2025-01-27 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookapp', '0008_alter_weight_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='family',
            field=models.ForeignKey(blank=True, db_column='Family_ID', null=True, on_delete=django.db.models.deletion.CASCADE, to='cookapp.familymember'),
        ),
    ]
