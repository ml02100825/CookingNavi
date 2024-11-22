# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

# models.pyで定義したUserをインポート
from .models import Material,Cook,Recipe,Cookimage,Image


class RecipeAddForm(forms.Form):
    name = forms.CharField(label="料理名",max_length=50)
    type = forms.ChoiceField(label="種別", choices=[('1', '主菜'), ('2', '副菜'), ('3', 'その他')])
    recipe_text = forms.CharField(label="作り方")
    image1 = forms.ImageField(label="画像1")
    image2 = forms.ImageField(label="画像2")
    image3 = forms.ImageField(label="画像3")
    
