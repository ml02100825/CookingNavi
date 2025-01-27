from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth import login,authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreation1Form, CustomUserCreation2Form, LoginForm
from .models import User, Userallergy 
from cookapp.models import Familymember, Weight
from django.urls import reverse_lazy
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        logging.debug('debug message')
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.debug('if文動いてる')
            email = form.cleaned_data['email']  # 入力されたデータをセッションに保存
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user:
                # `DeleteFlag` チェック
                if user.deleteflag:
                    logging.warning(f"ユーザー {user.email} は退会済みのためログインを拒否しました。")
                    form.add_error(None, "This account has been deactivated. Please contact support.")
                else:
                    # is_activeが0でもログインできるように変更
                    if not user.is_active:  # ユーザーが無効状態でも
                        logging.debug(f"ユーザー {user.email} は非アクティブですがログイン処理を行います。")
                        user.is_active = 1  # is_active を 1 に変更
                        user.save()
                        logging.debug(f"ユーザー {user.email} の is_active を 1 に設定しました。")
                    
                    # ログイン処理を実行
                    login(request, user)
                    logging.debug(f"ユーザー {user.email} がログインしました。")
                    
                    request.session['user_id'] = user.user_id
                    request.session.modified = True
                    logging.debug(f"Session info: {request.session.items()}")  # セッション内容をログに出力
                    
                    # 管理者または一般ユーザーのリダイレクト先を決定
                    if user.is_superuser:
                        return redirect('administrator:home')
                    return redirect('cookapp:home')
            else:
                form.add_error(None, "Invalid username or password.")
        
        # フォームにエラーがある場合
        return render(request, self.template_name, {'form': form})

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
        form = CustomUserCreation1Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # 非アクティブユーザーの状態をチェック
            try:
                user = User.objects.get(email=email)
                if not user.is_active or user.DeleteFlag:
                    # 非アクティブまたは削除ユーザーの場合、次の画面へ遷移
                    logging.debug(f"非アクティブまたは削除ユーザー {email} を検出。次の画面へ遷移します。")
            except User.DoesNotExist:
                pass  # 新規ユーザーはそのまま処理を続行

            # セッションにデータを保存
            request.session['email'] = email
            request.session['password1'] = password
            return redirect('account:signup2')  # 次のページへ

        # フォームが無効な場合
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
 
            try:
                # 既存ユーザーを取得
                user = User.objects.get(email=email)
 
                # 非アクティブまたは論理削除ユーザーの場合、復活処理
                if not user.is_active or user.deleteflag:
                    user.is_active = 1  # アクティブ化
                    user.deleteflag = 0  # deleteflagを0に設定
                    user.set_password(password)  # 新しいパスワードを保存
                    logging.debug(f"非アクティブまたは削除ユーザー {email} を復活しました。")
 
                    # 必要なフィールドの更新
                    user.name = form.cleaned_data['name']
                    user.age = form.cleaned_data['birthdate']
                    user.gender = form.cleaned_data['gender']
                    user.height = form.cleaned_data['height']
                    user.weight = form.cleaned_data['weight']
                    user.save()
 
                else:
                    raise User.DoesNotExist  # 通常の新規作成へ進む
 
            except User.DoesNotExist:
                # 新規ユーザー作成
                hashed_password = make_password(password)
                user = User(
                    name=form.cleaned_data['name'],
                    email=email,
                    password=hashed_password,
                    age=form.cleaned_data['birthdate'],
                    gender=form.cleaned_data['gender'],
                    height=form.cleaned_data['height'],
                    weight=form.cleaned_data['weight'],
                )
                user.save()

            # 生年月日から年齢を計算
            birthdate = form.cleaned_data['birthdate']
            today = datetime.today().date()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

            # familymemberテーブルに登録
            family_member = Familymember(
                family_name=form.cleaned_data['name'],
                family_gender=form.cleaned_data['gender'],
                family_age=age,
                family_height=form.cleaned_data['height'],
                family_weight=form.cleaned_data['weight'],
                user=user  # userオブジェクトを使用
            )
            family_member.save()
            # weightテーブルに登録
            weight_entry = Weight(
                weight=form.cleaned_data['weight'],
                register_time=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                user=user,  # userオブジェクトを使用
                family=family_member  # familyオブジェクトを使用
            )
            weight_entry.save()
            # アレルギー情報の登録または更新
            allergies = form.cleaned_data['allergies']
            for allergy in allergies:
                Userallergy.objects.update_or_create(
                    user=user, allergy_category=allergy
                )
 
            # ログイン処理
            login(request, user)
            return redirect('account:signup_completion')  # 完了画面へ遷移
 
        # フォームが無効な場合
        return render(request, self.template_name, {'form': form})

class CustomSignUpView(TemplateView):
    template_name = 'administrator/sign up/sign up_completion.html'


class CustomLogoutView(LogoutView):
    template_name = 'logout/logout.html'
    # ログアウト後に 'account:login_ok' にリダイレクト
    next_page = reverse_lazy('account:logout_ok')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                # is_active を 0 に変更
                user = request.user
                user.is_active = 0
                user.save()
                logging.debug(f"ユーザー {user.email} の is_active を 0 に設定しました。")
            except Exception as e:
                logging.error(f"ログアウト中にエラーが発生しました: {e}")
        return super().dispatch(request, *args, **kwargs)
    
class LogoutOkView(TemplateView):
    template_name = 'logout/logout_ok.html'


class IndexView(TemplateView):
    template_name = 'top/top.html'