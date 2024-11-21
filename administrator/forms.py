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
    materials =  forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label="材料を選択",
        to_field_name='name',
    )
       # オブジェクトの表示内容を変更する
    def label_from_instance(self, obj):
        return f"{obj.name}"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materials'].widget.attrs.update({
            'class': 'form-control',
            'id': 'materialselect',
        })

    
