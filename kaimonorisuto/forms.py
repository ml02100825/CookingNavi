from django import forms

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        label='開始日',
        widget=forms.DateInput(attrs={'type': 'date'}),  # HTML5の日付入力フィールド
    )
    end_date = forms.DateField(
        label='終了日',
        widget=forms.DateInput(attrs={'type': 'date'}),  # 同じく日付入力フィールド
    )
