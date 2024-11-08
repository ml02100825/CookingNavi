from django.utils import timezone
from django.db import models

class User(models.Model):
    user_id = models.CharField(verbose_name="ユーザID", db_column='User_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    name = models.CharField(verbose_name="ユーザ名", db_column='Name', max_length=30)  # Field name made lowercase.
    password = models.CharField(verbose_name="パスワード", db_column='Password', max_length=512)  # Field name made lowercase.
    email = models.EmailField(verbose_name="メールアドレス", db_column='email', unique=True, max_length=128)  # Field name made lowercase.
    gender = models.CharField(verbose_name="性別", db_column='Gender', max_length=1)  # Field name made lowercase.
    age = models.CharField(verbose_name="生年月日", db_column='Age', max_length=10)  # Field name made lowercase.
    height = models.FloatField(verbose_name="身長", db_column='Height')  # Field name made lowercase.
    weight = models.FloatField(verbose_name="体重", db_column='Weight')  # Field name made lowercase.
    is_superuser = models.BooleanField(verbose_name="管理者フラグ", db_column='is_superuser')  # Field name made lowercase.
    family = models.BooleanField(verbose_name="家族フラグ", db_column='Family')  # Field name made lowercase.
    last_login = models.DateTimeField(verbose_name="ログイン日時", db_column='last_login')  # Field name made lowercase.
    deleteflag = models.BooleanField(verbose_name="削除フラグ", db_column='DeleteFlag')  # Field name made lowercase.
    subscribeflag = models.BooleanField(verbose_name="サブスクフラグ", db_column='SubscribeFlag')  # Field name made lowercase.
    subjoin = models.CharField(verbose_name="サブスク入会日付", db_column='SubJoin', max_length=20, blank=True, null=True)  # Field name made lowercase.
    unsub = models.CharField(verbose_name="サブスク退会日付", db_column='UnSub', max_length=20, blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(verbose_name="ログインフラグ",db_column='is_active')
    date_joined = models.DateTimeField(verbose_name="入会日付",db_column='date_joined',auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()
    class Meta:
        managed = False
        db_table = 'user'
    
    
