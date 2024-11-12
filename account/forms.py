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
    birthdate = forms.DateField(label="生年月日", widget=forms.SelectDateWidget(years=range(1900, 2025)))
    gender = forms.ChoiceField(label="性別", choices=[('male', '男性'), ('female', '女性'), ('other', 'その他')])
    allergies = forms.CharField(label="アレルギー", required=False)
    height = forms.FloatField(label="身長 (cm)", min_value=0)
    weight = forms.FloatField(label="体重 (kg)", min_value=0)

    class Meta:
        model = User
        fields = ('birthdate', 'gender', 'allergies', 'height', 'weight')
    
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
      
