# Generated by Django 4.2.5 on 2025-01-27 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookapp', '0009_alter_weight_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='family',
            field=models.ForeignKey(db_column='Family_ID', default=1, on_delete=django.db.models.deletion.CASCADE, to='cookapp.familymember'),
            preserve_default=False,
        ),
    ]
