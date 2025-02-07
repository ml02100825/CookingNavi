from django import forms
from django.forms.widgets import DateInput
from django.utils import timezone



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
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        # 入力されたパスワードが一致するか確認
        if new_password != confirm_password:
            self.add_error('confirm_password', "パスワードが一致しません。")
        
        return cleaned_data
    

class BodyInfoUpdateForm(forms.Form):
    name = forms.CharField(label='名前', max_length=20)
    birthdate = forms.DateField(label="生年月日", widget=forms.SelectDateWidget(years=range(1900, 2025)))
    gender = forms.ChoiceField(label="性別", choices=[('1', '男性'), ('2', '女性'), ('3', 'その他')])
    allergies = forms.MultipleChoiceField(
        label="アレルギー",
        choices=[
            ('1', 'えび'), ('2', 'かに'), ('3', 'くるみ'), ('4', '小麦'), ('5', 'そば'),
            ('6', '卵'), ('7', '乳'), ('8', '落花生(ピーナッツ)'), ('9', 'アーモンド'),
            ('10', 'あわび'), ('11', 'いか'), ('12', 'いくら'), ('13', 'オレンジ'), ('14', 'カシューナッツ'),
            ('15', 'キウイフルーツ'), ('16', '牛肉'), ('17', 'ごま'), ('18', '鮭'), ('19', '鯖'),
            ('20', '大豆'), ('21', '鶏肉'), ('22', 'バナナ'), ('23', '豚肉'), ('24', 'マカダミアナッツ'),
            ('25', 'もも'), ('26', 'やまいも'), ('27', 'りんご'), ('28', 'ゼラチン')
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    height = forms.FloatField(label="身長 (cm)", min_value=0)
    weight = forms.FloatField(label="体重 (kg)", min_value=0)
    

class FamilyForm(forms.Form):
    family_name = forms.CharField(label='名前', max_length=20)

    # 生年月日入力 (カレンダーウィジェット)
    birth_date = forms.DateField(
        label='生年月日',
        widget=DateInput(attrs={'type': 'date'}),  # HTML5 のカレンダーウィジェット
        input_formats=['%Y-%m-%d'],  # 入力形式を指定
    )

    family_gender = forms.ChoiceField(
        label='性別',
        choices=[('0', '男性'), ('1', '女性'), ('2', 'その他')],
    )
    family_height = forms.FloatField(label='身長')
    family_weight = forms.FloatField(label='体重')

    # アレルギー情報（複数選択可能）
    allergy_id = forms.MultipleChoiceField(
        label='アレルギー',
        choices=[
            ('1', 'エビ'),
            ('2', '小麦'),
            ('3', 'くるみ'),
            ('4', 'カニ'),
            ('5', 'そば'),
            ('6', '卵'),
            ('7', '牛乳'),
            ('8', '落花生'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False  # オプショナル
    )

    # 年齢計算用のメソッド
    def calculate_age(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            today = timezone.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        return None

    def clean_allergy_id(self):
        allergy_id = self.cleaned_data.get('allergy_id')
        if not allergy_id:
            return []  # 'なし'が選ばれた場合は空リストとして扱う
        return allergy_id


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))