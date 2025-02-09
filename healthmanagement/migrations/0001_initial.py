# Generated by Django 4.2.6 on 2025-02-05 02:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("administrator", "0001_initial"),
    ]

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
                (
                    "user",
                    models.ForeignKey(
                        db_column="User_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "menu",
            },
        ),
        migrations.CreateModel(
            name="Menucook",
            fields=[
                (
                    "menucook_id",
                    models.AutoField(
                        db_column="menucook_ID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "cook",
                    models.ForeignKey(
                        db_column="Cook_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.cook",
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        db_column="Menu_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="healthmanagement.menu",
                    ),
                ),
            ],
            options={
                "db_table": "menucook",
            },
        ),
    ]
