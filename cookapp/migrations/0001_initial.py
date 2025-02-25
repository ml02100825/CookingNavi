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
            name="Allergy",
            fields=[
                (
                    "allergy_id",
                    models.AutoField(
                        db_column="ALLERGY_ID",
                        primary_key=True,
                        serialize=False,
                        verbose_name="アレルギーID",
                    ),
                ),
                (
                    "material_id",
                    models.IntegerField(db_column="MATERIAL_ID", verbose_name="材料ID"),
                ),
                (
                    "allergy_category",
                    models.CharField(
                        db_column="ALLERGY_CATEGORY",
                        max_length=30,
                        verbose_name="アレルギーカテゴリー",
                    ),
                ),
                (
                    "allergy_name",
                    models.CharField(
                        db_column="ALLERGY_NAME", max_length=30, verbose_name="アレルギー名"
                    ),
                ),
            ],
            options={
                "db_table": "allergy",
            },
        ),
        migrations.CreateModel(
            name="Familymember",
            fields=[
                (
                    "family_id",
                    models.AutoField(
                        db_column="Family_ID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "family_name",
                    models.CharField(db_column="Family_Name", max_length=30),
                ),
                (
                    "family_gender",
                    models.CharField(db_column="Family_Gender", max_length=1),
                ),
                ("family_age", models.CharField(db_column="Family_Age", max_length=10)),
                (
                    "family_height",
                    models.DecimalField(
                        db_column="Family_Height", decimal_places=2, max_digits=5
                    ),
                ),
                (
                    "family_weight",
                    models.DecimalField(
                        db_column="Family_Weight", decimal_places=2, max_digits=5
                    ),
                ),
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
                "db_table": "familymember",
            },
        ),
        migrations.CreateModel(
            name="News",
            fields=[
                (
                    "news_id",
                    models.AutoField(
                        db_column="NEWS_ID", primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(db_column="title", max_length=100)),
                ("content", models.TextField(db_column="Content")),
                (
                    "upload_time",
                    models.CharField(db_column="UploadTime", max_length=20),
                ),
                (
                    "update_time",
                    models.CharField(
                        blank=True, db_column="UpdateTime", max_length=20, null=True
                    ),
                ),
                ("subscribe", models.CharField(db_column="Subscribe", max_length=1)),
            ],
            options={
                "db_table": "News",
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "question_id",
                    models.IntegerField(
                        db_column="Qustion_ID", primary_key=True, serialize=False
                    ),
                ),
                ("question", models.TextField(db_column="Qustion")),
                ("answer", models.TextField(db_column="Answer")),
            ],
            options={
                "db_table": "Question",
            },
        ),
        migrations.CreateModel(
            name="Weight",
            fields=[
                (
                    "weight_id",
                    models.AutoField(
                        db_column="Weight_ID", primary_key=True, serialize=False
                    ),
                ),
                ("weight", models.FloatField(db_column="Weight")),
                (
                    "register_time",
                    models.CharField(db_column="RegisterTime", max_length=50),
                ),
                (
                    "family",
                    models.ForeignKey(
                        db_column="Family_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cookapp.familymember",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="User_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weights",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "weight",
            },
        ),
        migrations.CreateModel(
            name="Newsimage",
            fields=[
                (
                    "newsimage_id",
                    models.AutoField(
                        db_column="NEWSIMAGE_ID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        db_column="IMAGE_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrator.image",
                    ),
                ),
                (
                    "news",
                    models.ForeignKey(
                        db_column="NEWS_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cookapp.news",
                    ),
                ),
            ],
            options={
                "db_table": "NewsImage",
            },
        ),
        migrations.CreateModel(
            name="Familyallergy",
            fields=[
                (
                    "family_allergy_id",
                    models.AutoField(
                        db_column="FamilyAllergyID",
                        primary_key=True,
                        serialize=False,
                        verbose_name="家族アレルギーID",
                    ),
                ),
                (
                    "allergy",
                    models.ForeignKey(
                        db_column="Allergy_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cookapp.allergy",
                        verbose_name="アレルギー",
                    ),
                ),
                (
                    "family_member",
                    models.ForeignKey(
                        db_column="Family_ID",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cookapp.familymember",
                        verbose_name="家族",
                    ),
                ),
            ],
            options={
                "db_table": "familyallergy",
            },
        ),
    ]
