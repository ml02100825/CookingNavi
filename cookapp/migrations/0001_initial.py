# Generated by Django 4.2.5 on 2024-11-15 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(db_column='User_ID', primary_key=True, serialize=False, verbose_name='ユーザID')),
                ('name', models.CharField(db_column='Name', max_length=30, verbose_name='ユーザ名')),
                ('password', models.CharField(db_column='Password', max_length=512, verbose_name='パスワード')),
                ('email', models.EmailField(db_column='email', max_length=128, unique=True, verbose_name='メールアドレス')),
                ('gender', models.CharField(db_column='Gender', max_length=1, verbose_name='性別')),
                ('age', models.CharField(db_column='Age', max_length=10, verbose_name='生年月日')),
                ('height', models.FloatField(db_column='Height', verbose_name='身長')),
                ('weight', models.FloatField(db_column='Weight', verbose_name='体重')),
                ('is_superuser', models.BooleanField(db_column='is_superuser', default=False, verbose_name='管理者フラグ')),
                ('is_staff', models.BooleanField(db_column='is_staff', default=False, verbose_name='管理者フラグ')),
                ('family', models.BooleanField(db_column='Family', default=False, verbose_name='家族フラグ')),
                ('last_login', models.DateTimeField(auto_now=True, db_column='last_login', verbose_name='ログイン日時')),
                ('deleteflag', models.BooleanField(db_column='DeleteFlag', default=False, verbose_name='削除フラグ')),
                ('subscribeflag', models.BooleanField(db_column='SubscribeFlag', default=False, verbose_name='サブスクフラグ')),
                ('subjoin', models.CharField(blank=True, db_column='SubJoin', max_length=20, null=True, verbose_name='サブスク入会日付')),
                ('unsub', models.CharField(blank=True, db_column='UnSub', max_length=20, null=True, verbose_name='サブスク退会日付')),
                ('is_active', models.BooleanField(db_column='is_active', default=True, verbose_name='ログインフラグ')),
                ('date_joined', models.DateTimeField(auto_now_add=True, db_column='date_joined', verbose_name='入会日付')),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Userallergy',
            fields=[
                ('userallergy_id', models.AutoField(auto_created=True, db_column='USERALLERGY_ID', primary_key=True, serialize=False, verbose_name='ユーザアレルギーID')),
                ('allergy_category', models.CharField(db_column='ALLERGY_CATEGORY', max_length=10)),
            ],
            options={
                'db_table': 'userallergy',
                'managed': False,
            },
        ),
    ]