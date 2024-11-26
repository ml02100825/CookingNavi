from django.db import models

# Create your models here.
class Material(models.Model):
    material_id = models.AutoField(db_column='MATERIAL_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=55)  # Field name made lowercase.
    calorie = models.CharField(db_column='Calorie', max_length=10)  # Field name made lowercase.
    protein = models.CharField(db_column='Protein', max_length=10)  # Field name made lowercase.
    lipids = models.CharField(db_column='Lipids', max_length=10)  # Field name made lowercase.
    fiber = models.CharField(db_column='Fiber', max_length=10)  # Field name made lowercase.
    carbohydrates = models.CharField(db_column='Carbohydrates', max_length=10)  # Field name made lowercase.
    saltcontent = models.CharField(db_column='SaltContent', max_length=10)  # Field name made lowercase.
    
    def __str__(self):
        return self.name  # nameだけを表示
    
    class Meta:
        managed = False
        db_table = 'material'
        
class Cook(models.Model):
    cook_id = models.AutoField(db_column='Cook_ID', primary_key=True)  # Field name made lowercase.
    cookname = models.CharField(db_column='CookName', max_length=50)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=1)  # Field name made lowercase.
    recipe_text = models.TextField(db_column='RECIPE_TEXT')  # Field name made lowercase.
    calorie = models.FloatField(db_column='Calorie')  # Field name made lowercase.
    protein = models.FloatField(db_column='Protein')  # Field name made lowercase.
    lipids = models.FloatField(db_column='LIPIDS')  # Field name made lowercase.
    carbohydrates = models.FloatField(db_column='Carbohydrates')  # Field name made lowercase.
    fiber = models.FloatField(db_column='Fiber')  # Field name made lowercase.
    saltcontent = models.FloatField(db_column='SaltContent')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cook'
class Recipe(models.Model):
    recipe_id = models.AutoField(db_column='RECIPE_ID', primary_key=True)  # Field name made lowercase.
    cook = models.ForeignKey('Cook', models.PROTECT, db_column='COOK_ID')  # Field name made lowercase.
    material = models.ForeignKey('Material', models.PROTECT, db_column='MATERIAL_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recipe'
        
class Image(models.Model):
    image_id = models.AutoField(db_column='Image_ID', primary_key=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'image'
        
        
class Cookimage(models.Model):
    cookimage_id = models.AutoField(db_column='COOKIMAGE_ID', primary_key=True)  # Field name made lowercase.
    cook = models.ForeignKey('Cook', models.CASCADE, db_column='COOK_ID')  # Field name made lowercase.
    image = models.ForeignKey('Image', models.SET_NULL, db_column='IMAGE_ID', null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cookimage'



class CookImagesave(models.Model):
    
    image = models.ImageField(upload_to='cook/')  # 画像の保存先フォルダ
    
