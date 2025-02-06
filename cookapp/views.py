import json
from django.shortcuts import get_object_or_404, render, redirect

from administrator.models import Cookimage, Recipe
from healthmanagement.models import Menu, Menucook
from .forms import EmailForm, UsernameForm, PasswordForm, BodyInfoUpdateForm, FamilyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from .models import Familymember, Familyallergy, News, Question, Weight
from account.models import  Userallergy 
from django.http import JsonResponse
import logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.urls import reverse
import calendar
import json
from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import PasswordResetDoneView
from datetime import datetime
from urllib.parse import unquote

 
 
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
                User = get_user_model()
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
    def get(self, request, *args, **kwargs):
        user = request.user
        news = News.objects.all().values('news_id','title','update_time', 'content').order_by('update_time')
        newslist = list(news)
        logging.debug(newslist)
        context = {
            'news': news,
        }
        return render(request, self.template_name, context)
        
 
class QuestionsView(TemplateView):
    template_name='questions/questions.html'
    def get(self, request, *args, **kwargs):
        question = Question.objects.all().values('question_id','question','answer').order_by('question_id')
        questionlist = list(question)
        logging.debug(questionlist)
        context = {
            'question': questionlist,
        }
        return render(request, self.template_name, context)
 
 
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

                user = authenticate(email=user.email, password=new_password)
                if user is not None:
                    login(request, user)

                return redirect('cookapp:password_henko_ok')  # プロフィールページなどにリダイレクト
       
        return render(request, self.template_name, {'form': form})
 
class PasswordOkView(TemplateView):
    template_name = 'acount/password/password_henko_ok.html'
 
 
class BodyInfoUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'sintai/sintai_henko.html'

    def get(self, request, *args, **kwargs):
        initial_data = {
            'name': request.user.name,
            'birthdate': request.user.age,
            'gender': request.user.gender,
            'height': request.user.height,
            'weight': request.user.weight,
            'allergies': [ua.allergy for ua in Userallergy.objects.filter(user=request.user)]
        }
        form = BodyInfoUpdateForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})
   
    def post(self, request, *args, **kwargs):
        family_member = Familymember.objects.filter(user=request.user).first()
        form = BodyInfoUpdateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            birthdate = form.cleaned_data['birthdate']
            gender = form.cleaned_data['gender']
            allergies = form.cleaned_data['allergies']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            logging.debug(birthdate)
            modified_birthdate = str(birthdate).replace("-", "/")

            if name != request.user.name:
                messages.error(request, "ログイン中のユーザーと異なるユーザー名を入力しました。")
            else:
                user = request.user
                user.age = modified_birthdate
                user.gender = gender
                user.height = height
                user.weight = weight
                user.save()
                logging.debug(modified_birthdate)

                # 既存のアレルギー情報を削除
                Userallergy.objects.filter(user=user).delete()

                # 新しいアレルギー情報を登録
                for allergy in allergies:
                    Userallergy.objects.create(user=user, allergy=allergy)

                weight_entry = Weight(
                    weight=form.cleaned_data['weight'],
                    register_time=timezone.now().strftime('%Y-%m-%d'),
                    user=user,  # userオブジェクトを使用
                    family_id=family_member.family_id,  # familyオブジェクトを使用
                )
                weight_entry.save()

                return redirect('cookapp:body_info_ok')
       
        return render(request, self.template_name, {'form': form})
       
class BodyInfoOkView(TemplateView):
    template_name = 'sintai/sintai_henko_ok.html'
 
class FamilyInfoView(LoginRequiredMixin, TemplateView):
    template_name = 'kazoku/kazoku.html'

    def get(self, request, *args, **kwargs):
        # ログインユーザーに関連する家族情報を取得
        family_members = Familymember.objects.filter(user=request.user).exclude(family_name=request.user.name)

        # family_name と family_id を渡す
        family_data = [{'name': member.family_name, 'id': member.family_id} for member in family_members]

        context = {
            'family_members': family_data,
        }

        return render(request, self.template_name, context)
 
   
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
            family_age = form.cleaned_data['birth_date']
            formatted_age = family_age.strftime("%Y/%m/%d")
            family_gender = form.cleaned_data['family_gender']
            family_height = form.cleaned_data['family_height']
            family_weight = form.cleaned_data['family_weight']
            allergy_ids = form.cleaned_data.get('allergy_id')


            # 家族情報を登録
            family_member = Familymember.objects.create(
                family_name=family_name,
                family_age=formatted_age,
                family_gender=family_gender,
                family_height=family_height,
                family_weight=family_weight,
                user=request.user._wrapped if hasattr(request.user, '_wrapped') else request.user  # SimpleLazyObject を解決
            )

            # Weightテーブルにデータを登録
            Weight.objects.create(
                weight=family_weight,  # Familymember の weight を登録
                user=family_member.user,  # Familymember の user を登録
                family_id=family_member.family_id,  # 数値の family_id を登録
                register_time=datetime.now().strftime('%Y-%m-%d')  # 今日の日付を登録
            )

            # 家族アレルギー情報を登録
            for allergy_id in allergy_ids:
                Familyallergy.objects.create(
                    family_member=family_member,
                    allergy_id=allergy_id
                )

            if family_member and request.user.family == False:
                user = request.user
                user.family = True
                user.save()

            # 登録完了後のリダイレクト
            return redirect('cookapp:kazoku_add_ok')

        # フォームが無効な場合
        return render(request, self.template_name, {'form': form})




    
class KazokuaddOkView(TemplateView):
    template_name = 'kazoku/add/kazoku_add_ok.html'


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .forms import FamilyForm
from .models import Familymember, Familyallergy, Allergy  # Allergy モデルをインポート

class KazokuHenkoView(LoginRequiredMixin, TemplateView):
    template_name = 'kazoku/henko/kazoku_henko.html'

    def get(self, request, *args, **kwargs):
        # 編集する家族メンバーの取得
        family_member = Familymember.objects.get(family_id=kwargs['family_id'])
        # フォームの初期値を設定
        initial_data = {
            'family_name': family_member.family_name,
            'family_gender': family_member.family_gender,
            'family_height': family_member.family_height,
            'family_weight': family_member.family_weight,
            'allergy_id': [fa.allergy_id for fa in Familyallergy.objects.filter(family_member=family_member)]
        }
        form = FamilyForm(initial=initial_data)
        return render(request, self.template_name, {'form': form, 'family_member': family_member})

    def post(self, request, *args, **kwargs):
        family_member = Familymember.objects.get(family_id=kwargs['family_id'])
        form = FamilyForm(request.POST)

        if form.is_valid():
            # フォームデータを取得
            family_name = form.cleaned_data['family_name']
            family_gender = form.cleaned_data['family_gender']
            family_height = form.cleaned_data['family_height']
            family_weight = form.cleaned_data['family_weight']
            allergy_ids = form.cleaned_data.get('allergy_id')

            # 家族メンバーを更新
            family_member.family_name = family_name
            family_member.family_gender = family_gender
            family_member.family_height = family_height
            family_member.family_weight = family_weight
            family_member.save()

            # Weightテーブルに新しいレコードを追加
            Weight.objects.create(
                weight=family_weight,  # 更新された体重を登録
                user=family_member.user,  # 家族メンバーに紐づくユーザー
                family=family_member,  # 家族メンバー
                register_time=timezone.now().strftime('%Y-%m-%d')  # 今日の日付を登録
            )

            # 既存のアレルギー情報を削除
            Familyallergy.objects.filter(family_member=family_member).delete()

            # 新しいアレルギー情報を登録
            for allergy_id in allergy_ids:
                Familyallergy.objects.create(
                    family_member=family_member,  # 家族情報インスタンス
                    allergy_id=allergy_id         # アレルギーID
                )

            # 更新後のリダイレクト
            return redirect('cookapp:kazoku_henko_ok', family_id=family_member.family_id)

        # フォームが無効な場合もフォームを再表示
        return render(request, self.template_name, {'form': form, 'family_member': family_member})
    
class KazokuHenkoOkView(TemplateView):
    template_name = 'kazoku/henko/kazoku_henko_ok.html'
 
    def get(self, request, family_id, *args, **kwargs):
        # family_idに基づいて家族情報を取得
        family_member = Familymember.objects.get(family_id=family_id)
        return render(request, self.template_name, {'family_member': family_member})
 
 
class DietaryHistoryView(TemplateView):
    template_name = 'shokujirireki/dietaryhistory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 今日の日付を取得
        today = datetime.today().date()

        # すべてのメニューを取得（降順に並べ替え）、今日以降の日付を除外
        menus = Menu.objects.filter(meal_day__lt=today).order_by('-meal_day')
        
        # メニューに関連する料理を取得
        menu_cooks = Menucook.objects.filter(menu__in=menus)
        
        # 料理名を日付ごとに整理
        cook_names = {}
        missing_menus = set(menus.values_list('menu_id', 'meal_day', 'mealtime')) - set(menu_cooks.values_list('menu_id', 'menu__meal_day', 'menu__mealtime'))
        
        for menu in menus:
            meal_day = str(menu.meal_day)
            meal_time = '朝' if menu.mealtime == '0' else '昼' if menu.mealtime == '1' else '晩'
            
            if meal_day not in cook_names:
                cook_names[meal_day] = {'朝': [], '昼': [], '晩': []}
            
            related_cooks = menu_cooks.filter(menu=menu)
            if related_cooks.exists():
                for menu_cook in related_cooks:
                    cook_names[meal_day][meal_time].append(menu_cook.cook.cookname)
            else:
                cook_names[meal_day][meal_time].append(None)


        # 逆順で並べて、最初に昨日を表示する
        sorted_cook_names = dict(sorted(cook_names.items(), reverse=True))

        # コンテキストにデータを追加
        context['cook_names'] = sorted_cook_names
        context['missing_menus'] = missing_menus
        return context

class DietaryHistoryDetailView(TemplateView):
    template_name = 'shokujirireki/dietaryhistorydetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = kwargs.get('date')
        cookname = unquote(kwargs.get('cookname'))
        
        print(f"DEBUG: date={date}, cookname={cookname}")  # デバッグ用
        
        # 日付と料理名に基づいてメニューを取得
        menu_cooks = Menucook.objects.filter(menu__meal_day=date, cook__cookname__icontains=cookname)

        print(f"DEBUG: menu_cooks={menu_cooks}")  # デバッグ用
        print(f"DEBUG: SQL Query: {menu_cooks.query}")

        if not menu_cooks.exists():
            context['error_message'] = "該当する料理情報が見つかりませんでした。"
        else:
            context['menu_cooks'] = menu_cooks
            # 画像と材料を取得してコンテキストに追加
            for menu_cook in menu_cooks:
                cook_images = Cookimage.objects.filter(cook=menu_cook.cook)
                menu_cook.cook.images = [ci.image.image for ci in cook_images if ci.image]
                recipes = Recipe.objects.filter(cook=menu_cook.cook)
                menu_cook.cook.materials = [(recipe.material.name, recipe.quantity) for recipe in recipes]

        return context
 
 
class HealthGraphView(TemplateView):
    template_name = 'kenkougurahu/healthgraph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        family_members = Familymember.objects.filter(user=user)
        family_members = list(family_members)  # クエリセットをリストに変換
        context['family_members'] = family_members
        return context

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            family_id = data.get('family_id')
            start_date = data.get('start_date')

            if not family_id or not start_date:
                return JsonResponse({'error': '家族と日付を選択してください。'}, status=400)

            try:
                year, month = map(int, start_date.split('-'))
            except ValueError:
                return JsonResponse({'error': '無効な日付フォーマットです。'}, status=400)

            first_day = datetime(year, month, 1)
            last_day = datetime(year, month, calendar.monthrange(year, month)[1])

            try:
                family_id = int(family_id)
            except ValueError:
                return JsonResponse({'error': '無効な家族IDです。'}, status=400)

            weights = Weight.objects.filter(
                family_id=family_id,
                register_time__gte=first_day,
                register_time__lte=last_day
            ).order_by('register_time')

            if not weights:
                return JsonResponse({'error': '指定した期間の体重データはありません。'}, status=404)
            
            dates = [datetime.strptime(weight.register_time, '%Y-%m-%d').strftime('%Y-%m-%d') for weight in weights]
            weight_values = [weight.weight for weight in weights]

            return JsonResponse({"dates": dates, "weights": weight_values})
        except Exception as e:
            logging.error(f"Error in HealthGraphView post: {e}")
            return JsonResponse({'error': '内部サーバーエラーが発生しました。'}, status=500)
   
 
@login_required
def confirm_taikai(request):
    if request.method == 'POST':
        # ログアウトして退会処理
        user = request.user
        user.deleteflag = True  # ユーザーの無効化（退会状態にする）
        user.save()
        logout(request)  # ログアウト処理
        return redirect('cookapp:taikai_ok')  # ホームページなど任意のページにリダイレクト
 
    return render(request, 'taikai/taikai.html')

@login_required
def taikai_ok(request):
    return render(request, 'taikai/taikai_ok.html')
 
@login_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')  # ダッシュボードのテンプレートを指定
    
class KazokuKakuninView(TemplateView):
    template_name = 'kazoku/kakunin/kazoku_kakunin.html'

    def get(self, request, family_id):
        try:
            # 家族メンバーの情報を取得
            family_member = Familymember.objects.get(family_id=family_id)
            # 関連するアレルギーIDを取得
            allergies = Familyallergy.objects.filter(family_member=family_member)
            
            # allergy_idを使用してアレルギー名に変換する辞書を作成
            allergy_names = []
            allergy_mapping = {
                1: 'エビ',  # allergy_idが1の場合は「エビ」
                2: '小麦',    # allergy_idが2の場合は「卵」
                3: 'くるみ',  # allergy_idが3の場合は「小麦」
                4: 'カニ', # allergy_idが4の場合は「ナッツ」
                5: 'そば',
                6: '卵',
                7: '牛乳',
                8: '落花生',
                # 必要に応じて他のアレルギーIDも追加
            }

            # allergiesからallergy_idを取得して、対応するアレルギー名をリストに追加
            for allergy in allergies:
                allergy_name = allergy_mapping.get(allergy.allergy_id, '不明')  # マッピングがない場合は「不明」
                allergy_names.append(allergy_name)

        except Familymember.DoesNotExist:
            return redirect('cookapp:kazoku')  # 家族情報が存在しない場合、家族一覧ページにリダイレクト

        return render(request, 'kazoku/kakunin/kazoku_kakunin.html', {'family_member': family_member, 'allergy_names': allergy_names})

    
class KazokuSakujoView(TemplateView):
    template_name = 'kazoku/sakujo/kazoku_sakujo.html'

    def get(self, request, *args, **kwargs):
        family_id = kwargs['family_id']
        family_member = get_object_or_404(Familymember, family_id=family_id)  # 修正: family_idを使用
        return self.render_to_response({'family_member': family_member})

    def post(self, request, *args, **kwargs):
        family_id = kwargs['family_id']
        family_member = get_object_or_404(Familymember, family_id=family_id)  # 修正: family_idを使用

        # 関連するFamilyallergyデータを削除
        Familyallergy.objects.filter(family_member=family_member).delete()

        # Familymemberデータを削除
        family_member.delete()
        return redirect(reverse('cookapp:kazoku_sakujo_ok', kwargs={'family_id': family_id}))
    
class KazokuSakujoOkView(TemplateView):
    template_name = 'kazoku/sakujo/kazoku_sakujo_ok.html'


class KiyakuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'kiyaku/kiyaku.html')
    
# PasswordResetDoneViewのカスタマイズが必要な場合
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

# 通常のビューが必要な場合
def password_reset_done_view(request):
    return render(request, 'registration/password_reset_done.html')