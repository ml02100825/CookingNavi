from django import forms
from .models import Bbs, Postimage

class BbsForm(forms.ModelForm):
    class Meta:
        model = Bbs
        fields = ['name', 'recipe_text']
    
    # 画像をフォームに追加する
    image = forms.ImageField(required=False)  # 画像フィールド（任意）

    def save(self, commit=True):
        bbs_instance = super().save(commit=False)

        if commit:
            bbs_instance.save()
        
        # 画像の保存処理
        image = self.cleaned_data.get('image')
        if image:
            postimage = Postimage(post=bbs_instance, image=image)
            postimage.save()
        
        return bbs_instance

class RecipeAddForm(forms.Form):
    name = forms.CharField(label="料理名", max_length=50)
    recipe_text = forms.CharField(
        label="作り方", 
        widget=forms.Textarea(attrs={"placeholder": "作り方を記入", "rows": 4})
    )
    image1 = forms.ImageField(label="画像1", required=False)
    image2 = forms.ImageField(label="画像2", required=False)
    image3 = forms.ImageField(label="画像3", required=False)
