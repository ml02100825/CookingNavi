# UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

# models.pyで定義したUserをインポート
from .models import Material,Cook


class RecipeAddForm(forms.ModelForm):
    name = forms.CharField()
    class Meta:
        model =Cook
        fields = ('name', 'recipe_text', 'allergies', 'type')