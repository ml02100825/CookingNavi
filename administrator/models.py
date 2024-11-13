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

    class Meta:
        managed = False
        db_table = 'material'
        
class Cook(models.Model):
    cook_id = models.IntegerField(db_column='Cook_ID', primary_key=True)  # Field name made lowercase.
    cookname = models.CharField(db_column='CookName', max_length=10)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=1)  # Field name made lowercase.
    recipe_text = models.TextField(db_column='RECIPE_TEXT')  # Field name made lowercase.
    carorie = models.FloatField(db_column='Carorie', db_comment='カロリー')  # Field name made lowercase.
    protein = models.FloatField(db_column='Protein', db_comment='たんぱく質')  # Field name made lowercase.
    lipids = models.FloatField(db_column='LIPIDS', db_comment='脂質')  # Field name made lowercase.
    carbohydrates = models.FloatField(db_column='Carbohydrates', db_comment='炭水化物')  # Field name made lowercase.
    fiber = models.FloatField(db_column='Fiber', db_comment='食物繊維')  # Field name made lowercase.
    saltcontent = models.FloatField(db_column='SaltContent', db_comment='塩分含有量')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cook'