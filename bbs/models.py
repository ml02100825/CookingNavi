from django.db import models
from account.models import User

# Create your models here.
class Bbs(models.Model):
    post_id = models.AutoField(db_column='POST_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('account.User', models.CASCADE, db_column='USER_ID')  # Field name made lowercase.
    recipe_text = models.TextField(db_column='RECIPE_TEXT')  # Field name made lowercase.
    post_time = models.CharField(db_column='POST_TIME', max_length=20)  # Field name made lowercase.
    update_time = models.CharField(db_column='UPDATE_TIME', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bbs'

class Postimage(models.Model):
    postimage_id = models.AutoField(db_column='POSTIMAGE_ID', primary_key=True)  # Field name made lowercase.
    post = models.ForeignKey('Bbs', models.DO_NOTHING, db_column='POST_ID')  # Field name made lowercase.
    image = models.ForeignKey('administrator.Image', models.DO_NOTHING, db_column='IMAGE_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'postimage'


class Userrecipe(models.Model):
    userrecipe_id = models.AutoField(db_column='USERRECIPE_ID', primary_key=True)  # Field name made lowercase.
    post = models.ForeignKey('Bbs', models.DO_NOTHING, db_column='POST_ID')  # Field name made lowercase.
    material = models.ForeignKey('administrator.Material', models.DO_NOTHING, db_column='MATERIAL_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userrecipe'