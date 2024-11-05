from django.db import models

# Create your models here.
class User(models.Modek):
    userid = models.CharField(
        verbose_name= "ユーザID",
        max_length=10
    )
    name = models.CharField(
        verbose_name = "ユーザ名",
        max_length = 30
    )
    password = models.CharField(
        verbose_name= "パスワード",
        max_length= 512
    )
    mailaddress = models.CharField(
        verbose_name= "メールアドレス",
        max_length= 128
    )
    gender = models.CharField(
        verbose_name= "性別",
        max_length= 1
    )
    age = models.CharField(
        verbose_name= "生年月日",
        max_length= 10
    )
    height = models.DecimalField(
        verbose_name= "身長",
        max_length= 10
    )
    weight = models.DecimalField(
        verbose_name= "体重",
        max_length= 10
    )
    admin = models.BooleanField(
        verbose_name= "管理者フラグ",
        max_length= 10
    )
    familyflag = models.BooleanField(
        verbose_name= "家族フラグ",
        max_length= 10
    )
    logoutfkag = models.BooleanField(
        verbose_name="ログアウトフラグ",
        max_length= 10
    )
    
     
    