from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreation1Form, CustomUserCreation2Form, LoginForm
from .models import User, Userallergy
from django.urls import reverse_lazy
import logging

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        logging.debug('debug message')
        form =  LoginForm(request.POST)
        if form.is_valid():
            logging.debug('if文動いてる')
            email = form.cleaned_data['email'] # 入力されたデータをセッションに保存
            password= form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    
                    if request.user.is_authenticated:
 
                        logging.debug('loginできてる')
                    request.session['user_id'] = user.user_id
                    request.session.modified = True 
                    logging.debug(f"Session info: {request.session.items()}")  # セッション内容をログに出力
                    if user.is_superuser:
                        return redirect('administrator:home')
                    return redirect('cookapp:home')
            else:
                form.add_error(None, "Invalid username or password.")
    # redirect_authenticated_user = True
    # success_url = reverse_lazy('cookapp:index')

    # def get_success_url(self):
    #     return self.success_url


class SignUpPage1View(TemplateView):
    template_name = 'administrator/sign up/sign up.html'
    def get(self, request, *args, **kwargs):
        form = CustomUserCreation1Form()
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
            email = request.session.get('email')
            password = request.session.get('password1')
           
            # ユーザー作成
            hashed_password = make_password(password)
            userallergy = Userallergy.objects.create
            name = form.cleaned_data['name']

            # フォームの入力内容でユーザーの詳細情報を更新
            birthdate = form.cleaned_data['birthdate']
            gender = form.cleaned_data['gender']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            user = User(name = name,email = email, password = hashed_password, age = birthdate, gender = gender, height = height,weight = weight)
            user.save()
            allergies = form.cleaned_data['allergies']
            for i in range(len(allergies)):
                allergy = allergies[i]
                Userallergy.objects.create(user = user,allergy_category = allergy)

            # ログイン処理
            login(request, user)
   
            return redirect('account:signup_completion')
        return render(request, self.template_name, {'form': form})

class CustomSignUpView(TemplateView):
    template_name = 'administrator/sign up/sign up_completion.html'


class CustomLogoutView(LogoutView):
    # ログアウト後に表示するテンプレート（オプション）
    template_name = 'administrator/logout/logout.html'
    
    # ログアウト後に遷移するページ
    next_page = reverse_lazy('account:logout_ok')  

class LogoutOkView(TemplateView):
    template_name = 'administrator/logout/logout_completion.html'


class IndexView(TemplateView):
    template_name = 'top/top.html'