
from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
from django.views.generic.base import TemplateView
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password


from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreation1Form, CustomUserCreation2Form
from .models import User, Userallergy
from django.urls import reverse_lazy
import logging

class CustomLoginView(LoginView):
    template_name = 'login.html'  # ログインページのテンプレート
    redirect_authenticated_user = True  # ログイン済みユーザーをリダイレクト
    success_url = reverse_lazy('cookapp:index')  # ログイン後のリダイレクト先
    

    def get_success_url(self):
        # カスタムリダイレクト先を指定
        return self.success_url
    

class SignUpPage1View(TemplateView):
    template_name = 'administrator/sign up/sign up.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreation1Form() # もしセッションにデータがあれば、それをフォームに渡す
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        logging.debug('debug message')
        form = CustomUserCreation1Form(request.POST)
        if form.is_valid():
            logging.debug('if文動いてる')
            request.session['email'] = form.cleaned_data['email'] # 入力されたデータをセッションに保存
            request.session['password1'] = form.cleaned_data['password1']
            return redirect('account:signup2')  # 2ページ目へリダイレクト
        else:
          logging.debug('フォームが無効です: %s', form.errors) 
        return render(request, self.template_name, {'form': form})


class SignUpPage2View(TemplateView):
    template_name = 'administrator/sign up/sign up2.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreation2Form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreation2Form(request.POST)
        if form.is_valid():
            # セッションからメールアドレスとパスワードを取得
            email = request.session.get('email')
            password = request.session.get('password1')
          
            userallergy = Userallergy.objects.create
            hashed_password = make_password(password)
            # フォームの入力内容でユーザーの詳細情報を更新
            birthdate = form.cleaned_data['birthdate']
            gender = form.cleaned_data['gender']
            name = form.cleaned_data['name']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            user = User(name = name,email = email, password = hashed_password, age = birthdate, gender = gender, height = height,weight = weight)
            user.save()
          
            allergies = form.cleaned_data['allergies']
            for i in range(len(allergies)):
                allergy = allergies[i]
                Userallergy.objects.create(user = user,allergy_category = allergy)
            # ログイン処理
            user.backend = 'account.backends.EmailBackend' 
            login(request, user)
            return redirect('account:signup_completion')  # 登録完了ページへリダイレクト
        
        return render(request, self.template_name, {'form': form})

# 登録完了ページ
class CustomSignUpView(TemplateView):
    template_name = 'administrator/sign up/sign up_completion.html'
    

class CustomLogoutView(LogoutView):
    template_name = 'logout.html'  # ログアウトページのテンプレート


class IndexView(TemplateView):
    
    template_name='top/top.html'

class UsernameView(TemplateView):
    template_name='acount/name/username_henko.html'

class EmailView(TemplateView):
    template_name='acount/email/email_henko.html'

class PasswordView(TemplateView):
    template_name='acount/password/password_henko.html'