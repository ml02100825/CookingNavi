from django.shortcuts import render
from django.views.generic.base import TemplateView
from .forms import RecipeAddForm
from django.views.generic.edit import FormView
from django.views import View
# Create your views here.



class BulletinBoardView(TemplateView):
    template_name = 'keijiban/BulletinBoard.html'

class PostsView(TemplateView):
    template_name = 'keijiban/toukou/posts.html'
    form = RecipeAddForm  # フォームクラスを設定


class PostsView(View):
    template_name = 'keijiban/toukou/posts.html'

    def get(self, request):
        form = RecipeAddForm()  # フォームインスタンスを作成
        return render(request, self.template_name, {'form': form})