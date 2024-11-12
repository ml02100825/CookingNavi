# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
# models.pyで定義したUserをインポート
from .models import User

class CustomUserCreation1Form(UserCreationForm):
    email = forms.EmailField(required=True, label="メールアドレス")
    password1 = forms.CharField(widget=forms.PasswordInput, label="パスワード")
    password2 = forms.CharField(widget=forms.PasswordInput, label="パスワード確認")

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class CustomUserCreation2Form(forms.ModelForm):
    name = forms.CharField(label="ユーザ名", max_length=30)
    birthdate = forms.DateField(label="生年月日", widget=forms.SelectDateWidget(years=range(1900, 2025)))
    gender = forms.ChoiceField(label="性別", choices=[('1', '男性'), ('2', '女性'), ('3', 'その他')])
    allergies = forms.MultipleChoiceField(label="アレルギー", choices=[('1', 'えび'), ('2', 'かに'), ('3', 'くるみ'),
    ('4', '小麦'),('5', 'そば'),('6', '卵'),('7', '乳'),('8', '落花生(ピーナッツ)'),('9', 'アーモンド'),
    ('10', 'あわび'),('11', 'いか'),('12', 'いくら'),('13', 'オレンジ'),('14', 'カシューナッツ'),('15', 'キウイフルーツ'),
    ('16', '牛肉'),('17', 'ごま'),('18', '鮭'),('19', '鯖'),('20', '大豆'),('21', '鶏肉'),('22', 'バナナ'),('23', '豚肉'),('24', 'マカダミアナッツ'),
    ('25', 'もも'),('26', 'やまいも'),('27', 'りんご'),('28', 'ゼラチン'),],required=False, widget=forms.SelectMultiple(attrs={
            'size': '5'  # 表示する選択肢の数
        }))
    height = forms.FloatField(label="身長 (cm)", min_value=0)
    weight = forms.FloatField(label="体重 (kg)", min_value=0)

    class Meta:
        model = User
        fields = ('name','birthdate', 'gender', 'allergies', 'height', 'weight')
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = User

