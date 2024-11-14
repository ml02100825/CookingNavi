# Generated by Django 4.2.6 on 2024-11-13 03:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cook",
            fields=[
                (
                    "cook_id",
                    models.IntegerField(
                        db_column="Cook_ID", primary_key=True, serialize=False
                    ),
                ),
                ("cookname", models.CharField(db_column="CookName", max_length=10)),
                ("type", models.CharField(db_column="Type", max_length=1)),
                ("recipe_text", models.TextField(db_column="RECIPE_TEXT")),
                ("carorie", models.FloatField(db_column="Carorie", db_comment="カロリー")),
                ("protein", models.FloatField(db_column="Protein", db_comment="たんぱく質")),
                ("lipids", models.FloatField(db_column="LIPIDS", db_comment="脂質")),
                (
                    "carbohydrates",
                    models.FloatField(db_column="Carbohydrates", db_comment="炭水化物"),
                ),
                ("fiber", models.FloatField(db_column="Fiber", db_comment="食物繊維")),
                (
                    "saltcontent",
                    models.FloatField(db_column="SaltContent", db_comment="塩分含有量"),
                ),
            ],
            options={
                "db_table": "cook",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "material_id",
                    models.AutoField(
                        db_column="MATERIAL_ID", primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(db_column="Name", max_length=55)),
                ("calorie", models.CharField(db_column="Calorie", max_length=10)),
                ("protein", models.CharField(db_column="Protein", max_length=10)),
                ("lipids", models.CharField(db_column="Lipids", max_length=10)),
                ("fiber", models.CharField(db_column="Fiber", max_length=10)),
                (
                    "carbohydrates",
                    models.CharField(db_column="Carbohydrates", max_length=10),
                ),
                (
                    "saltcontent",
                    models.CharField(db_column="SaltContent", max_length=10),
                ),
            ],
            options={
                "db_table": "material",
                "managed": False,
            },
        ),
    ]
