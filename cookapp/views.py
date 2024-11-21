from django.shortcuts import get_object_or_404, render, redirect
from .forms import EmailForm, UsernameForm, PasswordForm, BodyInfoUpdateForm, FamilyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from .models import User, Userallergy, Familymember, Familyallergy, Weight
from django.contrib.auth.models import User
from django.http import JsonResponse
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
    template_name='health/health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health/health_selection.html'

class HealthSelectionComplateView(TemplateView):
    template_name='health/health_selectioncomplate.html'

class HealthMenuConfirmationView(TemplateView):
    template_name='health/health_menuconfirmation.html'

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


class NotificationSettingView(TemplateView):
    template_name='notification/notification.html'


class SubscriptionSettingView(TemplateView):
    template_name='sabusuku/setting/sabusuku_setting.html'

class SubscriptionLoginView(TemplateView):
    template_name='sabusuku/touroku/sabusuku_login.html'

class SubscriptionLoginOkView(LoginRequiredMixin, TemplateView):
    template_name='sabusuku/touroku/sabusuku_login_ok.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        # サブスク登録処理
        if user.subscribeflag:
            # subscribeflag が True の場合（入会済み）
            messages.warning(request, 'すでに入会済みです。')
            return redirect('cookapp:subscription_login')
        else:
            # subscribeflag が False の場合（未入会）
            user.subscribeflag = True  # サブスクフラグをTrueに設定
            user.subjoin = timezone.now().date()  # 入会日を現在の日付に設定
            user.save()

            # サブスク登録完了ページに遷移
            return render(request, self.template_name)

    
class SubscriptionKaiyakuView(TemplateView):
    template_name='sabusuku/kaiyaku/sabusuku_kaiyaku.html'

class SubscriptionKaiyakuOkView(LoginRequiredMixin, TemplateView):
    template_name='sabusuku/kaiyaku/sabusuku_kaiyaku_ok.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        # サブスク退会処理
        if user.subscribeflag:
            # subscribeflag が True の場合（入会済み）
            user.subscribeflag = False  # サブスクフラグをFalseに戻す
            user.unsub = timezone.now().date()  # 退会日を現在の日付に設定
            user.save()

            # サブスク解約完了ページに遷移
            return render(request, self.template_name)
        else:
            # subscribeflag が False の場合（未入会）
            messages.warning(request, '未入会です。')
            return redirect('cookapp:subscription_kaiyaku')


class OsiraseView(TemplateView):
    template_name='osirase/osirase.html'

class QuestionsView(TemplateView):
    template_name='questions/questions.html'


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

            if not request.user.check_password(current_password):
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
            name = form.cleaned_data['name']
            birthdate = form.cleaned_data['birthdate']
            gender = form.cleaned_data['gender']
            allergies = form.cleaned_data['allergies']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']

            if name != request.user.name:
                messages.error(request, "ログイン中のユーザーと異なるユーザー名を入力しました。")
            else:
                user = request.user
                user.age = birthdate
                user.gender = gender
                user.height = height
                user.weight = weight
                user.save()
                for i in range(len(allergies)):
                    allergy = allergies[i]
                    try:
                        # 既存のアレルギー情報を検索して更新する
                        user_allergy = Userallergy.objects.get(user=user, allergy_category=allergy)
                        user_allergy.allergy_category = allergy
                        user_allergy.save()  # 更新を保存
                        print(f"Updated allergy for user {user} with allergy {allergy}")
                    except Userallergy.DoesNotExist:
                        # レコードが見つからなかった場合の処理
                        print(f"Allergy {allergy} for user {user} not found, skipping.")

            return redirect('cookapp:body_info_ok')
        
        return render(request, self.template_name, {'form': form})
        
class BodyInfoOkView(TemplateView):
    template_name = 'sintai/sintai_henko_ok.html'

class FamilyInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'kazoku/kazoku.html'

    def get(self, request, *args, **kwargs):
        # ログインユーザーに関連する家族情報を取得
        family_members = Familymember.objects.filter(user=request.user)

        # family_name を明示的に取り出して渡す
        family_names = [member.family_name for member in family_members]
        
        # コンテキストに家族情報を追加
        context = {
            'family_members': family_names,  # family_names をテンプレートに渡す
        }

        return render(request, self.template_name, context)

    
class KazokuaddView(LoginRequiredMixin, TemplateView):
    template_name = 'kazoku/add/kazoku_add.html'

    # views.py
    def get(self, request, *args, **kwargs):
        form = FamilyForm()
        return render(request, self.template_name, {'form': form,})

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

class KazokuHenkoView(LoginRequiredMixin, TemplateView):
    template_name = 'kazoku/henko/kazoku_henko.html'

class HealthGraphView(TemplateView):
    template_name = 'kenkougurahu/healthgraph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ログインしているユーザーを取得
        user = self.request.user

        # ログインユーザーの家族情報を取得
        family_members = Familymember.objects.filter(user=user)

        # 家族メンバー情報をテンプレートに渡す
        context['family_members'] = family_members
        return context

    def post(self, request, *args, **kwargs):
        # ユーザーIDと開始日を取得
        user_id = request.POST.get('user_id')
        start_date = request.POST.get('start_date')

        if not user_id or not start_date:
            return JsonResponse({'error': 'ユーザーと日付を選択してください。'}, status=400)

        # ユーザーの体重データを取得
        weights = Weight.objects.filter(
            user_id=user_id,
            register_time__gte=start_date
        ).order_by('register_time')

        # 体重データが存在しない場合の処理
        if not weights:
            return JsonResponse({'error': '指定したユーザーの体重データはありません。'}, status=404)

        # 日付と体重のリストを作成
        dates = [weight.register_time.strftime('%Y-%m-%d') for weight in weights]
        weight_values = [weight.weight for weight in weights]

        # JSONでデータを返す
        return JsonResponse({
            'dates': dates,
            'weights': weight_values
        })

class DietaryHistoryView(TemplateView):
    template_name = 'shokujirireki/dietaryhistory.html'
