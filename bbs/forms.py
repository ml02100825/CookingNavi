from django import forms
from .models import Bbs
 
 
class RecipeAddForm(forms.Form):
    name = forms.CharField(label="料理名", max_length=50)
    recipe_text = forms.CharField(
        label="作り方",
        widget=forms.Textarea(attrs={"placeholder": "作り方を記入", "rows": 4})
    )
    image1 = forms.ImageField(label="画像1", required=False)
    image2 = forms.ImageField(label="画像2", required=False)
    image3 = forms.ImageField(label="画像3", required=False)
 
class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Bbs
        fields = ['name', 'recipe_text', 'calorie', 'protein', 'lipids', 'fiber', 'carbohydrates', 'saltcontent']
   
    # 画像フィールドは Bbs モデルにはなく、Postimage モデルで扱うため、フォームに追加しない
    image1 = forms.ImageField(label="画像1", required=False)
    image2 = forms.ImageField(label="画像2", required=False)
    image3 = forms.ImageField(label="画像3", required=False)