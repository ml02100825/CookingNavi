# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

# models.pyで定義したUserをインポート
from administrator.models import Cook


class CookSelectForm(forms.Form):
    CookSelect = forms.ModelChoiceField( queryset=Cook.objects.none(), #空のクエリセット
        widget=forms.widgets.Select)
    
