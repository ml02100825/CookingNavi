from django.utils import timezone
from django.db import models
from django.conf import settings



    
class Familymember(models.Model):
    family_id = models.AutoField(db_column='Family_ID', primary_key=True)
    family_name = models.CharField(db_column='Family_Name', max_length=30)
    family_gender = models.CharField(db_column='Family_Gender', max_length=1)
    family_age = models.CharField(db_column='Family_Age', max_length=10)
    family_height = models.FloatField(db_column='Family_Height')
    family_weight = models.FloatField(db_column='Family_Weight')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_column='User_ID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'familymember'



class Familyallergy(models.Model):
    family_allergy_id = models.AutoField(verbose_name='家族アレルギーID', db_column='FamilyAllergyID', primary_key=True)
    allergy = models.ForeignKey('Allergy', verbose_name='アレルギー', db_column='Allergy_ID', on_delete=models.CASCADE)
    family_member = models.ForeignKey('Familymember', verbose_name='家族', db_column='Family_ID', on_delete=models.CASCADE)
    
    class Meta:
        managed = False  # DB管理外
        db_table = 'familyallergy'

    def __str__(self):
        return f'{self.family_member.family_name} - {self.allergy.allergy_name}'

class Allergy(models.Model):
    allergy_id = models.AutoField(verbose_name='アレルギーID', db_column='ALLERGY_ID', primary_key=True)
    material_id = models.IntegerField(verbose_name='材料ID', db_column='MATERIAL_ID')
    allergy_category = models.CharField(verbose_name='アレルギーカテゴリー', db_column='ALLERGY_CATEGORY', max_length=30)
    allergy_name = models.CharField(verbose_name='アレルギー名', db_column='ALLERGY_NAME', max_length=30)

    class Meta:
        managed = False
        db_table = 'allergy'


class Weight(models.Model):
    weight_id = models.AutoField(db_column='Weight_ID', primary_key=True)
    weight = models.FloatField(db_column='Weight')
    register_time = models.CharField(db_column='RegisterTime', max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='User_ID', related_name='user_weights')
    family = models.ForeignKey(Familymember, db_column='Family_ID', on_delete=models.CASCADE)

    class Meta:
        db_table = 'weight'



