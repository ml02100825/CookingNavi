from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreation1Form, CustomUserCreation2Form, ChangeEmailForm,UsernameForm,LoginForm
from .models import User, Userallergy
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
import logging
from .forms import UsernameForm
from django.contrib.auth.hashers import check_password

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
            username = form.cleaned_data['username'] # 入力されたデータをセッションに保存
            password= form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('administrator:home')
                    else:
                        return redirect('cookapp:home')
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
    template_name = 'logout.html'
    next_page = reverse_lazy('account:top')

class IndexView(TemplateView):
    template_name = 'top/top.html'

class Username2View(TemplateView):
    template_name = 'acount/name/username_henko.html'

class UsernameView(FormView):
    form_class = UsernameForm
    login_url = reverse_lazy('account:login')

    def form_valid(self, form):
        new_username = form.cleaned_data["new_username"]
        confirm_username = form.cleaned_data["confirm_username"]

        if new_username == confirm_username:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE user SET Name = %s WHERE Name = %s", [new_username, self.request.user.id])
            return redirect("account:username_ok")
        else:
            form.add_error(None, "ユーザー名が一致しません")
            return self.form_invalid(form)

class UsernameOkView(TemplateView):
    template_name = "acount/name/username_henko_ok.html"

class EmailView(TemplateView):
    template_name = 'acount/acount/email/email_henko.html'

    def get(self, request, *args, **kwargs):
        form = ChangeEmailForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            
            # メールアドレスの更新
            user = request.user
            user.email = new_email
            user.save()

            messages.success(request, 'メールアドレスが正常に変更されました。')
            return redirect('account:profile')  # プロフィールページなどにリダイレクト
        
        return render(request, self.template_name, {'form': form})
    

class EmailHenkoView(TemplateView):
    template_name='acount/email/email_henko_ok.html'

class PasswordView(TemplateView):
    template_name = 'acount/password/password_henko.html'
