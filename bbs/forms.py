from django import forms
from administrator.models import Material  # 必要なモデルをインポート

class RecipeAddForm(forms.Form):
    name = forms.CharField(label="料理名", max_length=50)
    type = forms.ChoiceField(
        label="種別", 
        choices=[('1', '主菜'), ('2', '副菜'), ('3', 'その他')]
    )
    recipe_text = forms.CharField(
        label="作り方", 
        widget=forms.Textarea(attrs={"placeholder": "作り方を記入", "rows": 4})
    )
    image1 = forms.ImageField(label="画像1", required=False)
    image2 = forms.ImageField(label="画像2", required=False)
    image3 = forms.ImageField(label="画像3", required=False)
    
    # 材料を選択するためのフィールド
    materials = forms.ChoiceField(label="材料を選択")
