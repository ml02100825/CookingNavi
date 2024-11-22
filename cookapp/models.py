from django.utils import timezone
from django.db import models
from django.conf import settings


class User(models.Model):
    user_id = models.AutoField(verbose_name="ユーザID", db_column='User_ID', primary_key=True)
    name = models.CharField(verbose_name="ユーザ名", db_column='Name', max_length=30)
    password = models.CharField(verbose_name="パスワード", db_column='Password', max_length=512)
    email = models.EmailField(verbose_name="メールアドレス", db_column='email', unique=True, max_length=128)
    gender = models.CharField(verbose_name="性別", db_column='Gender', max_length=1)
    age = models.CharField(verbose_name="生年月日", db_column='Age', max_length=10)
    height = models.FloatField(verbose_name="身長", db_column='Height')
    weight = models.FloatField(verbose_name="体重", db_column='Weight')
    is_superuser = models.BooleanField(verbose_name="管理者フラグ", db_column='is_superuser', default=False)
    is_staff = models.BooleanField(verbose_name="スタッフフラグ", db_column='is_staff', default=False)
    family = models.BooleanField(verbose_name="家族フラグ", db_column='Family', default=False)
    last_login = models.DateTimeField(verbose_name="ログイン日時", db_column='last_login', auto_now=True)
    deleteflag = models.BooleanField(verbose_name="削除フラグ", db_column='DeleteFlag', default=False)
    subscribeflag = models.BooleanField(verbose_name="サブスクフラグ", db_column='SubscribeFlag', default=False)
    subjoin = models.CharField(verbose_name="サブスク入会日付", db_column='SubJoin', max_length=20, blank=True, null=True)
    unsub = models.CharField(verbose_name="サブスク退会日付", db_column='UnSub', max_length=20, blank=True, null=True)
    is_active = models.BooleanField(verbose_name="ログインフラグ", db_column='is_active', default=True)
    date_joined = models.DateTimeField(verbose_name="入会日付", db_column='date_joined', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def padded_id(self):
        return f"{self.user_id:010}"  # 10桁でゼロパディング

    class Meta:
        managed = False
        db_table = 'user'
    
    
class Familymember(models.Model):
    family_id = models.AutoField(verbose_name='家族ID', db_column='Family_ID', primary_key=True)
    family_name = models.CharField(verbose_name="名前", db_column='Family_Name', max_length=20)
    family_age = models.CharField(verbose_name='年齢', db_column='Family_Age', max_length=3)
    family_gender = models.CharField(verbose_name='性別', db_column='Family_Gender', max_length=3)
    family_height = models.FloatField(verbose_name='身長', db_column='Family_height')
    family_weight = models.FloatField(verbose_name='体重', db_column='Family_weight')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="family_members"
    )

    class Meta:
        managed = False
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
    weight_id = models.AutoField(verbose_name='体重ID', db_column='Weight_ID', primary_key=True)
    weight = models.FloatField(verbose_name='体重', db_column='Weight')
    register_time = models.DateTimeField(verbose_name='登録時間', db_column='RegisterTime')
    user_id = models.IntegerField(verbose_name='ユーザID', db_column='User_ID')
    family_id = models.IntegerField(verbose_name='家族ID', db_column='Family_ID')

    class Meta:
        managed = False
        db_table = 'weight'
        
