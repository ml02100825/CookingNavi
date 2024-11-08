
from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.views.generic.base import TemplateView


from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'  # ログインページのテンプレート
    redirect_authenticated_user = True  # ログイン済みユーザーをリダイレクト
    success_url = reverse_lazy('cookapp:index')  # ログイン後のリダイレクト先
    

    def get_success_url(self):
        # カスタムリダイレクト先を指定
        return self.success_url
    

class CustomLogoutView(LogoutView):
    template_name = 'logout.html'  # ログアウトページのテンプレート

class IndexView(TemplateView):
    
    template_name='top.html'