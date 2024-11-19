from django.utils import timezone
from django.db import models

class User(models.Model):
    user_id = models.AutoField(verbose_name="ユーザID", db_column='User_ID', primary_key=True,)  # Field name made lowercase.
    name = models.CharField(verbose_name="ユーザ名", db_column='Name', max_length=30)  # Field name made lowercase.
    password = models.CharField(verbose_name="パスワード", db_column='Password', max_length=512)  # Field name made lowercase.
    email = models.EmailField(verbose_name="メールアドレス", db_column='email', unique=True, max_length=128)  # Field name made lowercase.
    gender = models.CharField(verbose_name="性別", db_column='Gender', max_length=1)  # Field name made lowercase.
    age = models.CharField(verbose_name="生年月日", db_column='Age', max_length=10)  # Field name made lowercase.
    height = models.FloatField(verbose_name="身長", db_column='Height')  # Field name made lowercase.
    weight = models.FloatField(verbose_name="体重", db_column='Weight')  # Field name made lowercase.
    is_superuser = models.BooleanField(verbose_name="管理者フラグ", db_column='is_superuser',default = False)  # Field name made lowercase.
    is_staff = models.BooleanField(verbose_name="管理者フラグ", db_column='is_staff',default = False)  # Field name made lowercase.
    family = models.BooleanField(verbose_name="家族フラグ", db_column='Family',default = False)  # Field name made lowercase.
    last_login = models.DateTimeField(verbose_name="ログイン日時", db_column='last_login',auto_now=True)  # Field name made lowercase.
    deleteflag = models.BooleanField(verbose_name="削除フラグ", db_column='DeleteFlag',default = False)  # Field name made lowercase.
    subscribeflag = models.BooleanField(verbose_name="サブスクフラグ", db_column='SubscribeFlag',default = False)  # Field name made lowercase.
    subjoin = models.CharField(verbose_name="サブスク入会日付", db_column='SubJoin', max_length=20, blank=True, null=True)  # Field name made lowercase.
    unsub = models.CharField(verbose_name="サブスク退会日付", db_column='UnSub', max_length=20, blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(verbose_name="ログインフラグ",db_column='is_active',default = True)
    date_joined = models.DateTimeField(verbose_name="入会日付",db_column='date_joined',auto_now_add=True)
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
    
    
class Userallergy(models.Model):
    userallergy_id = models.AutoField(verbose_name="ユーザアレルギーID",db_column='USERALLERGY_ID', primary_key=True,   auto_created=True,)  # Field name made lowercase.
    user = models.ForeignKey('User', models.CASCADE, db_column='USER_ID')  # Field name made lowercase.
    allergy_category = models.CharField(db_column='ALLERGY_CATEGORY', max_length=10)  # Field name made lowercase.
    def padded_id(self):
        return f"{self.userallergy_id:010}"  # 10桁でゼロパディング
    class Meta:
        managed = False
        db_table = 'userallergy'


class Familymember(models.Model):
    family_id = models.AutoField(verbose_name='家族ID', db_column='Family_ID', primary_key=True)
    family_name = models.CharField(verbose_name="名前", db_column='Family_Name', max_length=20)
    family_age = models.CharField(verbose_name='年齢', db_column='Family_Age', max_length=3)
    family_gender = models.CharField(verbose_name='性別', db_column='Family_Gender', max_length=3)
    family_height = models.FloatField(verbose_name='身長', db_column='Family_height')
    family_weight = models.FloatField(verbose_name='体重', db_column='Family_weight')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー", db_column='User_ID') 
    class Meta:
        managed = False
        db_table = 'familymember'

class Familyallergy(models.Model):
    family_allergy_id = models.AutoField(verbose_name='家族アレルギーID', db_column='FamilyAllergyID', primary_key=True)
    allerg_id = models.CharField(verbose_name='アレルギーID', db_column='Allergy_ID', max_length=3)
    family_id = models.CharField(verbose_name='家族ID', db_column='Family_ID',max_length=50)
    class Meta:
        managed = False
        db_table = 'familyallergy'
