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