# UserCreationFormクラスをインポート
from django import forms

# models.pyで定義したUserをインポート
from .models import User

class CustomUserCreation1Form(forms.Form):
    email = forms.EmailField(required=True, label="メールアドレス")
    password1 = forms.CharField(widget=forms.PasswordInput, label="パスワード")
    password2 = forms.CharField(widget=forms.PasswordInput, label="パスワード確認")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active or user.deleteflag:  # 非アクティブまたは削除ユーザーの場合
                return email
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        except User.DoesNotExist:
            return email  # 新規登録の場合


class CustomUserCreation2Form(forms.ModelForm):
    name = forms.CharField(label="ユーザ名", max_length=30)
    birthdate = forms.DateField(label="生年月日", widget=forms.SelectDateWidget(years=range(1900, 2025)))
    gender = forms.ChoiceField(label="性別", choices=[('1', '男性'), ('2', '女性'), ('3', 'その他')])
    allergies = forms.MultipleChoiceField(
        label="アレルギー",
        choices=[('1', 'えび'), ('2', 'かに'), ('3', 'くるみ'), ('4', '小麦'), ('5', 'そば'),
                 ('6', '卵'), ('7', '乳'), ('8', '落花生(ピーナッツ)'), ('9', 'アーモンド')],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    height = forms.FloatField(label="身長 (cm)", min_value=0)
    weight = forms.FloatField(label="体重 (kg)", min_value=0)

    class Meta:
        model = User
        fields = ('name', 'birthdate', 'gender', 'allergies', 'height', 'weight')

    
class LoginForm(forms.Form):
    email=forms.EmailField(label='Email',max_length=30)
    password=forms.CharField(label='Password',widget=forms.PasswordInput())