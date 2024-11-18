from django.contrib.auth.hashers import check_password
from django import forms

class BodyInfoUpdateForm(forms.Form):
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


class UsernameForm(forms.Form):
    new_username = forms.CharField(max_length=150, label="新しいユーザー名")
    confirm_username = forms.CharField(max_length=150, label="新しいユーザー名（確認用）")

    def clean(self):
        cleaned_data = super().clean()
        new_username = cleaned_data.get("new_username")
        confirm_username = cleaned_data.get("confirm_username")

        # 入力されたユーザー名が一致するか確認
        if new_username != confirm_username:
            self.add_error('confirm_username', "ユーザー名が一致しません。")
        
        return cleaned_data


class EmailForm(forms.Form):
    new_email = forms.EmailField(max_length=254, label="新しいメールアドレス")
    confirm_email = forms.EmailField(max_length=254, label="新しいメールアドレス（確認用）")

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get("new_email")
        confirm_email = cleaned_data.get("confirm_email")

        # 入力されたメールアドレスが一致するか確認
        if new_email != confirm_email:
            self.add_error('confirm_email', "メールアドレスが一致しません。")
        
        return cleaned_data
    

class PasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="現在のパスワード")
    new_password = forms.CharField(max_length=150,  label="新しいパスワード")
    confirm_password = forms.CharField(max_length=150, label="新しいパスワード（確認用）")

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        # ユーザー情報を取得
        user = self.initial.get('user')

        if user and not user.check_password(current_password):
            self.add_error('current_password', "現在のパスワードが間違っています。")

        # 入力されたパスワードが一致するか確認
        if new_password != confirm_password:
            self.add_error('confirm_password', "パスワードが一致しません。")
        
        return cleaned_data