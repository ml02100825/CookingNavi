# Generated by Django 4.2.6 on 2025-01-22 01:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                (
                    "menu_id",
                    models.AutoField(
                        db_column="Menu_ID", primary_key=True, serialize=False
                    ),
                ),
                ("meal_day", models.DateField(db_column="Meal_Day", max_length=10)),
                ("mealtime", models.CharField(db_column="MealTime", max_length=1)),
            ],
            options={
                "db_table": "menu",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Menucook",
            fields=[
                (
                    "menuccok_id",
                    models.AutoField(
                        db_column="menuccok_ID", primary_key=True, serialize=False
                    ),
                ),
            ],
            options={
                "db_table": "menucook",
                "managed": False,
            },
        ),
    ]
