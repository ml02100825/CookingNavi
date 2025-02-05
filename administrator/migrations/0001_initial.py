# Generated by Django 4.2.6 on 2025-02-05 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cook",
            fields=[
                (
                    "cook_id",
                    models.AutoField(
                        db_column="Cook_ID", primary_key=True, serialize=False
                    ),
                ),
                ("cookname", models.CharField(db_column="CookName", max_length=50)),
                ("type", models.CharField(db_column="Type", max_length=1)),
                ("recipe_text", models.TextField(db_column="RECIPE_TEXT")),
                ("calorie", models.FloatField(db_column="Calorie")),
                ("protein", models.FloatField(db_column="Protein")),
                ("lipids", models.FloatField(db_column="LIPIDS")),
                ("carbohydrates", models.FloatField(db_column="Carbohydrates")),
                ("fiber", models.FloatField(db_column="Fiber")),
                ("saltcontent", models.FloatField(db_column="SaltContent")),
            ],
            options={
                "db_table": "cook",
            },
        ),
        migrations.CreateModel(
            name="Cookimagesave",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("image", models.ImageField(upload_to="cook/")),
            ],
            options={
                "db_table": "cookimagesave",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "image_id",
                    models.AutoField(
                        db_column="Image_ID", primary_key=True, serialize=False
                    ),
                ),
                ("image", models.CharField(db_column="Image", max_length=256)),
            ],
            options={
                "db_table": "image",
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
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "recipe_id",
                    models.AutoField(
                        db_column="RECIPE_ID", primary_key=True, serialize=False
                    ),
                ),
                ("quantity", models.IntegerField(db_column="material_quantity")),
                (
                    "cook",
                    models.ForeignKey(
                        db_column="COOK_ID",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="administrator.cook",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        db_column="MATERIAL_ID",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="administrator.material",
                    ),
                ),
            ],
            options={
                "db_table": "recipe",
            },
        ),
        migrations.CreateModel(
            name="Cookimage",
            fields=[
                (
                    "cookimage_id",
                    models.AutoField(
                        db_column="COOKIMAGE_ID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "cook",
                    models.ForeignKey(
                        db_column="COOK_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.cook",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        db_column="IMAGE_ID",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.image",
                    ),
                ),
            ],
            options={
                "db_table": "cookimage",
            },
        ),
    ]
