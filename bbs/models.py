from django.db import models
from account.models import User

class Bbs(models.Model):
    post_id = models.AutoField(db_column='POST_ID', primary_key=True)
    user = models.ForeignKey('account.User', models.DO_NOTHING, related_name='bbs_posts')  # db_columnを削除
    name = models.CharField(db_column='name', max_length=60)
    recipe_text = models.TextField(db_column='RECIPE_TEXT')
    post_time = models.DateTimeField(db_column='POST_TIME', auto_now_add=True)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', blank=True, null=True, auto_now=True)
    calorie = models.FloatField(db_column='calorie')
    protein = models.FloatField(db_column='protein')
    lipids = models.FloatField(db_column='lipids')
    fiber = models.FloatField(db_column='fiber')
    carbohydrates = models.FloatField(db_column='carbohydrates')
    saltcontent = models.FloatField(db_column='saltcontent')

    class Meta:
        managed = False
        db_table = 'bbs'


class Postimage(models.Model):
    postimage_id = models.AutoField(db_column='POSTIMAGE_ID', primary_key=True)
    post = models.ForeignKey('Bbs', models.DO_NOTHING, db_column='POST_ID')
    image = models.ForeignKey('administrator.Image', models.DO_NOTHING, db_column='IMAGE_ID')

    class Meta:
        managed = False
        db_table = 'postimage'


class Image(models.Model):
    image_id = models.AutoField(db_column='IMAGE_ID', primary_key=True)  # データベースの主キー列を指定
    bbs = models.ForeignKey(Bbs, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')  # 画像ファイル保存先
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'image'  # 正しいテーブル名を指定

    def __str__(self):
        return self.name


class Userrecipe(models.Model):
    userrecipe_id = models.AutoField(db_column='USERRECIPE_ID', primary_key=True)  # Field name made lowercase.
    post = models.ForeignKey('Bbs', models.DO_NOTHING, db_column='POST_ID')  # Field name made lowercase.
    material = models.ForeignKey('administrator.Material', models.DO_NOTHING, db_column='MATERIAL_ID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='material_quantity')
    class Meta:
        managed = False
        db_table = 'userrecipe'
