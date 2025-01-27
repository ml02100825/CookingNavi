# Generated by Django 4.2.5 on 2025-01-24 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0002_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(db_column='IMAGE_ID', primary_key=True, serialize=False)),
                ('image', models.ImageField(db_column='image', upload_to='images/')),
            ],
            options={
                'db_table': 'image',
                'managed': False,
            },
        ),
    ]
