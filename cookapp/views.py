from django.shortcuts import get_object_or_404, render, redirect
from .forms import EmailForm, UsernameForm, PasswordForm, BodyInfoUpdateForm, FamilyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from account.models import User, Userallergy
from .models import Familymember, Familyallergy
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name='index.html'

class CustomLogin1View(TemplateView):
    template_name='Login1.html'

class HomeView(TemplateView):
    template_name='home/home.html'
    def get(self, request, *args, **kwargs):
        logging.debug(f"Session info: {self.request.session.items()}")  # セッション内容をログに出力
        logging.debug(f"User is authenticated: {request.user.is_authenticated}")
        return super().get(request, *args, **kwargs)
    # def get_context_data(self, **kwargs):
    #     logging.debug(f"User ID: {self.request.user.id}")
    #     user = self.request.user  # または request.user

    #     # ユーザーIDでデータベースから再取得することも可能
    #     id = self.request.session.get('_auth_user_id')
    #     user = User.objects.get(user_id=id)
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = user  # ログインしているユーザー情報を渡す
    #     return context

class HealthMainView(TemplateView):
    template_name='health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health_selection.html'

class SettingView(TemplateView):
    template_name='setting/setting.html'
    

class AcountSettingView(TemplateView):
    def dispatch(self,request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            logger.error("Error 401: Unauthorized access attempt to AccountSettingView.")
            logging.debug(f"Session info: {request.session.items()}")  # セッション内容をログに出力
             # ログインしていない場合はリダイレクト
        return super().dispatch(request,*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_id' in self.request.session:
            id = self.request.session['user_id']
            try:
                user = User.objects.get(user_id=id)
                context['user'] = user
            except User.DoesNotExist:
                context['user'] = None
        else:
            context['user'] = None
             
        return context
    template_name='acount/acount_setting.html'

class FamilyInfoView(TemplateView):
    template_name='kazoku/kazoku.html'

class NotificationSettingView(TemplateView):
    template_name='notification/notification.html'

class SubscriptionSettingView(TemplateView):
    template_name='sabusuku/setting/sabusuku_setting.html'

class OsiraseView(TemplateView):
    template_name='osirase/osirase.html'

class QuestionsView(TemplateView):
    template_name='questions/questions.html'


class UsernameView(TemplateView):
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
            user.name = new_username
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
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            if current_password != request.user.password:
                messages.error(request, "ログイン中のユーザーと異なるパスワードを入力しました。")
            else:
                # パスワードの更新
                user = request.user
                user.set_password(new_password)
                user.save()

                messages.success(request, 'パスワードが正常に変更されました。')
            return redirect('cookapp:password_henko_ok')  # プロフィールページなどにリダイレクト
        
        return render(request, self.template_name, {'form': form})

class PasswordOkView(TemplateView):
    template_name = 'acount/password/password_henko_ok.html'


class BodyInfoUpdateView(LoginRequiredMixin, TemplateView):
    template_name='sintai/sintai_henko.html'
    def get(self, request, *args, **kwargs):
        form = BodyInfoUpdateForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, * args, **kwargs):
        form = BodyInfoUpdateForm(request.POST)
        if form.is_valid():
            birthdate = form.cleaned_data['birthdate']
            gender = form.cleaned_data['gender']
            allergies = form.cleaned_data['allergies']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']

            user = request.user
            user.age = birthdate
            user.gender = gender
            user.height = height
            user.weight = weight
            user.save()
                
            # 既存のアレルギー情報を削除して、新しい情報を追加
            user_allergies = Userallergy.objects.filter(user=user)
            user_allergies.delete()  # 現在のアレルギー情報を削除

            # 新しいアレルギー情報を追加
            for allergy in allergies:
                Userallergy.objects.create(user=user, allergy_category=allergy)
                print(f"Added new allergy {allergy} for user {user}")

            return redirect('cookapp:body_info_ok')
        
        return render(request, self.template_name, {'form': form})
        
class BodyInfoOkView(TemplateView):
    template_name = 'sintai/sintai_henko_ok.html'

    
class KazokuaddView(LoginRequiredMixin, TemplateView):
    template_name = 'kazoku/add/kazoku_add.html'

    def get(self, request, *args, **kwargs):
        form = FamilyForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FamilyForm(request.POST)
        if form.is_valid():
            # フォームデータを取得
            family_name = form.cleaned_data['family_name']
            birth_date = form.cleaned_data['birth_date']
            family_gender = form.cleaned_data['family_gender']
            family_height = form.cleaned_data['family_height']
            family_weight = form.cleaned_data['family_weight']
            allergy_id = form.cleaned_data.get('allergy_id')  # 選択されたアレルギーIDを取得

            # 生年月日から年齢を計算
            family_age = form.calculate_age()

            # 家族情報を登録
            family_member = Familymember.objects.create(
                family_name=family_name,
                family_age=family_age,  # 計算した年齢を登録
                family_gender=family_gender,
                family_height=family_height,
                family_weight=family_weight,
                user=request.user._wrapped if hasattr(request.user, '_wrapped') else request.user  # SimpleLazyObject を解決
            )

            # 家族アレルギー情報を登録（アレルギーIDが選択されている場合）
            if allergy_id:  # アレルギーが選択されている場合のみ登録
                Familyallergy.objects.create(
                    family_id=family_member.family_id,  # 追加した family_member の ID を使用
                    allergy_id=allergy_id
                )

            # メッセージ表示
            messages.success(request, '家族情報が正常に登録されました。')

            # 登録完了後のリダイレクト
            return redirect('cookapp:kazoku_add_ok')

        # フォームが無効な場合
        return render(request, self.template_name, {'form': form})
    
class KazokuaddOkView(TemplateView):
    template_name = 'kazoku/add/kazoku_add_ok.html'
    
