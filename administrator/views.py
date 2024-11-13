from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView




class HomeView(TemplateView):
    template_name='administrator/home/home.html'
class RecipeView(TemplateView):
    template_name = 'administrator/recipe/recipe.html'
class RecipeAddView(TemplateView):
    template_name = 'administrator/recipe/add/recipe_add.html'
    
