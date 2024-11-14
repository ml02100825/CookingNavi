from django.shortcuts import render, redirect
from .forms import EmailForm, UsernameForm, PasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages


class IndexView(TemplateView):
    template_name='index.html'

class CustomLogin1View(TemplateView):
    template_name='Login1.html'

class HomeView(TemplateView):
    template_name='home/home.html'

class HealthMainView(TemplateView):
    template_name='health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health_selection.html'

class SettingView(TemplateView):
    template_name='setting/setting.html'

class AcountSettingView(TemplateView):
    template_name='acount/acount_setting.html'

class FamilyInfoView(TemplateView):
    template_name='kazoku/kazoku.html'

class BodyInfoUpdateView(TemplateView):
    template_name='sintai/sintai_henko.html'

class NotificationSettingView(TemplateView):
    template_name='/.html'

class SubscriptionSettingView(TemplateView):
    template_name='sabusuku/setting/sabusuku_setting.html'


class UsernameView(LoginRequiredMixin, TemplateView):
    template_name = 'acount/name/username_henko.html'
    def get(self, request, *args, **kwargs):
        form = UsernameForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            
            # メールアドレスの更新
            user = request.user
            user.Name = new_username
            user.save()

            messages.success(request, 'ユーザー名が正常に変更されました。')
            return redirect('cookapp:username_henko_ok')  # プロフィールページなどにリダイレクト
        
        return render(request, self.template_name, {'form': form})

class UsernameOkView(TemplateView):
    template_name = "acount/name/username_henko_ok.html"


class EmailView(LoginRequiredMixin, TemplateView):
    template_name = 'acount/email/email_henko.html'
    def get(self, request, *args, **kwargs):
        form = EmailForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = EmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            
            # メールアドレスの更新
            user = request.user
            user.email = new_email
            user.save()

            messages.success(request, 'メールアドレスが正常に変更されました。')
            return redirect('cookapp:email_henko_ok')  # プロフィールページなどにリダイレクト
        
        return render(request, self.template_name, {'form': form})

class EmailOkView(TemplateView):
    template_name = 'acount/email/email_henko_ok.html'


class PasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'acount/password/password_henko.html'
    def get(self, request, *args, **kwargs):
        form = PasswordForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = PasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            
            # パスワードの更新
            user = request.user
            user.password = new_password
            user.save()

            messages.success(request, 'パスワードが正常に変更されました。')
            return redirect('cookapp:password_henko_ok')  # プロフィールページなどにリダイレクト
        
        return render(request, self.template_name, {'form': form})

class PasswordOkView(TemplateView):
    template_name = 'acount/password/password_henko_ok.html'