
from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
from django.views.generic.base import TemplateView
from django.contrib.auth import login


from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreation1Form, CustomUserCreation2Form
from .models import User
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'  # ログインページのテンプレート
    redirect_authenticated_user = True  # ログイン済みユーザーをリダイレクト
    success_url = reverse_lazy('cookapp:index')  # ログイン後のリダイレクト先
    

    def get_success_url(self):
        # カスタムリダイレクト先を指定
        return self.success_url
    

class SignUpPage1View(TemplateView):
    template_name = 'sign up.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreation1Form() # もしセッションにデータがあれば、それをフォームに渡す
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreation1Form(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data['email'] # 入力されたデータをセッションに保存
            request.session['password1'] = form.cleaned_data['password1']
            return redirect('sign up2')  # 2ページ目へリダイレクト
        return render(request, self.template_name, {'form': form})


class SignUpPage2View(TemplateView):
    template_name = 'sign up2.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreation2Form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreation2Form(request.POST)
        if form.is_valid():
            # セッションからメールアドレスとパスワードを取得
            email = request.session.get('email')
            password = request.session.get('password1')

            # ユーザー作成
            user = User.objects.create_user(email=email, password=password)
            
            # フォームの入力内容でユーザーの詳細情報を更新
            user.birthdate = form.cleaned_data['birthdate']
            user.gender = form.cleaned_data['gender']
            user.allergies = form.cleaned_data.get('allergies')
            user.height = form.cleaned_data['height']
            user.weight = form.cleaned_data['weight']
            user.save()

            # ログイン処理
            login(request, user)
            return redirect('sign up_completion')  # 登録完了ページへリダイレクト
        
        return render(request, self.template_name, {'form': form})
    

# 登録完了ページ
class CustomSignUpView(TemplateView):
    template_name = 'sign up_completion.html'
    

class CustomLogoutView(LogoutView):
    template_name = 'logout.html'  # ログアウトページのテンプレート


class IndexView(TemplateView):
    
    template_name='top.html'