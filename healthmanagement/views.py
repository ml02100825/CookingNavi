import random
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
import urllib
from account.models import Userallergy
from administrator.models import Cook, Cookimage, Image, Material, Recipe
from datetime import datetime, date, timedelta
from cookapp.models import Familymember, Familyallergy,Allergy
from .forms import CookSelectForm
from .models import Menu, Menucook
from django.utils import timezone
from django.urls import reverse
import json
from django.db.models import Max
import logging
    
def image_get(menu):
    menucook = Menucook.objects.filter(menu = menu['menu_id']).values('cook')
    for i in menucook:
        
        menuid = Cook.objects.filter(cook_id= i['cook']).values('cook_id', 'type')
        menuid = menuid[0]
        if menuid['type'] == '1':
                break
    menuimageid = Cookimage.objects.filter(cook =menuid['cook_id']).values('image')
    menuimageid= menuimageid[0]
    menuimage = Image.objects.filter(image_id =menuimageid['image']).values('image')
    menuimage = menuimage[0]
    menuimageurl= menuimage['image']
    logging.debug(menuimage)
    logging.debug(menuimageurl)
    return menuimageurl

def process_group_1_2(age,gender,weight):
    # 1-2歳の処理
    if gender == '0':
        Basal_metabolism = 61.0
        protein = 20
        saltcontent = 3.0
    else:
        Basal_metabolism = 59.7
        protein = 20
        saltcontent = 2.5
    calorie =Basal_metabolism * 1.35 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    fiber = 0
    logging.debug(calorie)
    return calorie, protein, libids, carbohydrates,fiber,saltcontent

def process_group_3_5(age,gender,weight):
    # 3-5歳の処理
    if gender == '0':
        Basal_metabolism = 54.8
        protein = 25
        saltcontent = 3.5
    else:
        Basal_metabolism = 52.2
        protein = 25
        saltcontent = 3.5
    calorie = Basal_metabolism * 1.45 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    fiber = 8
        
    return calorie,protein, libids, carbohydrates , fiber , saltcontent


def process_group_6_7(age,gender,weight):
    # 6-7歳の処理
    if gender == '0':
        Basal_metabolism = 44.3
        protein = 30
        fiber = 10
        saltcontent = 4.5
    else:
        Basal_metabolism = 41.9
        protein = 30
        fiber = 9
        saltcontent = 4.5
    calorie = Basal_metabolism * 1.55 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    
    return calorie, protein,libids,carbohydrates,fiber, saltcontent


def process_group_8_9(age,gender,weight):
    # 8-9歳の処理
    if gender == '0':
        Basal_metabolism = 40.8
        protein = 40
        saltcontent = 5.0
    else:
        Basal_metabolism = 38.3
        protein = 40
        saltcontent = 5.0
    calorie = Basal_metabolism * 1.6 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    fiber = 11
    return calorie , protein, libids , carbohydrates , fiber , saltcontent


def process_group_10_11(age,gender,weight):
    # 10-11歳の処理
    if gender == '0':
        protein = 45
        Basal_metabolism = 37.4
        saltcontent = 6.0
    else:
        Basal_metabolism = 34.8
        protein = 50
        saltcontent = 6.0
    calorie = Basal_metabolism * 1.65 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    fiber = 13
    return calorie, protein, libids, carbohydrates,fiber, saltcontent

def process_group_12_14(age,gender,weight):
    # 12-14歳の処理
    if gender == '0':
        protein = 60
        Basal_metabolism = 31.0
        fiber = 17
        saltcontent = 7.0
    else:
        Basal_metabolism = 29.6
        protein = 55
        fiber = 16
        saltcontent = 6.5
    calorie =Basal_metabolism * 1.70 *weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    return calorie, protein, libids,carbohydrates ,fiber, saltcontent

def process_group_15_17(age,gender,weight):
    # 15-17歳の処理
    if gender == '0':
        protein = 65
        Basal_metabolism = 27.0
        fiber = 19
        saltcontent = 7.5
    else:
        Basal_metabolism = 25.3
        protein = 55
        fiber = 18
        saltcontent = 6.5
    calorie = Basal_metabolism * 1.70 *weight
    libids = calorie * 0.2
    carbohydrates = calorie *0.5
    return calorie, protein, libids, carbohydrates, fiber, saltcontent

def process_group_18_29(age,gender,weight):
    # 18-29歳の処理
    if gender == '0':
        Basal_metabolism = 23.7
        protein = 65
        fiber = 20
        saltcontent = 7.5
    else:
        Basal_metabolism = 22.1
        protein = 50
        fiber = 18
        saltcontent = 6.5
    calorie =Basal_metabolism * 1.75 *weight
    libids = calorie * 0.2
    carbohydrates  = calorie * 0.5
    logging.debug(calorie)
    return calorie, protein, libids, carbohydrates, fiber, saltcontent

def process_group_30_49(age,gender,weight):
    # 30-49歳の処理
    if gender == '0':
        Basal_metabolism = 22.5
        protein = 65
        fiber = 22
        saltcontent = 7.5
    else:
        Basal_metabolism = 21.9
        protein = 50
        fiber = 18
        saltcontent = 6.5
    calorie = Basal_metabolism * 1.75* weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    return calorie, protein, libids,carbohydrates,fiber,saltcontent

def process_group_50_64(age,gender,weight):
    # 50-64歳の処理
    if gender == '0':
        Basal_metabolism = 21.8
        protein = 65
        fiber = 22
        saltcontent = 7.5
    else:
        Basal_metabolism = 20.7
        protein = 50
        fiber = 18
        saltcontent = 6.5
    calorie =Basal_metabolism * 1.75 *weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    return calorie, protein, libids,carbohydrates,fiber,saltcontent

def process_group_65_74(age,gender,weight):
    # 65-74歳の処理
    if gender == '0':
        Basal_metabolism = 21.6
        protein = 60
        fiber = 22
        saltcontent = 7.5
    else:
        Basal_metabolism = 20.7
        protein = 50
        fiber = 18
        saltcontent = 6.5
    calorie = Basal_metabolism * 1.7 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    return calorie, protein, libids,carbohydrates,fiber,saltcontent

def process_group_75_plus(age,gender,weight):
    # 75歳以上の処理
    if gender == '0':
        Basal_metabolism = 21.5
        protein = 60
        fiber = 20
        saltcontent = 7.5
    else:
        Basal_metabolism = 20.7
        protein = 50
        fiber = 17
        saltcontent = 6.5
    calorie = Basal_metabolism * 1.7 * weight
    libids = calorie * 0.2
    carbohydrates = calorie * 0.5
    return calorie, protein, libids , carbohydrates , fiber, saltcontent
   
class HealthMainView(TemplateView):
    template_name='health/health_management_main.html'
    
    def get(self, request, *args, **kwargs):
        today = datetime.today()
        # 7日分の日付を生成し、整数型の月日を渡す
        dates = [(today + timedelta(days=i)).strftime('%m-%d') for i in range(7)]

        menu_status = []
        for i in range(7):
            current_date = today + timedelta(days=i)
            # メニューがあるか確認（朝、昼、晩）
            exist_list = {
                '0': "T" if Menu.objects.filter(meal_day=current_date, mealtime='0', user=request.user).exists() else "F",  # 朝
                '1': "T" if Menu.objects.filter(meal_day=current_date, mealtime='1', user=request.user).exists() else "F",  # 昼
                '2': "T" if Menu.objects.filter(meal_day=current_date, mealtime='2', user=request.user).exists() else "F",  # 晩
            }
            menu_status.append({'date': dates[i], 'status': exist_list})

        # コンテキストに日付とそのメニュー状態を渡す
        return render(request, self.template_name, {'menu_status': menu_status})

class HealthMenuView(TemplateView):
    template_name = 'health/health_menuconfirmation.html'

    def get(self, request, *args, **kwargs):
        # 料理リスト
        cooklist = []
        # 材料リスト
        materiallist = []

        # 引数から取得された値を使用
        time = self.kwargs.get('time')  # 1: 朝, 2: 昼, 3: 晩
        day = self.kwargs.get('day')  # 選択された日付（文字列としてyyyy-mm-ddで渡されていると仮定）
        year = datetime.now().year  # 現在の年を使う
        formatted_day = f"{year}-{day}"  # '2025-01-31' の形式に変換

        # 渡された日付をdatetimeに変換
        currentday = date.fromisoformat(formatted_day)

        # メニュー情報を取得
        Cooks = Menu.objects.filter(user=request.user, meal_day=currentday, mealtime=time).values('menu_id')

        # メニューが存在する場合にそのメニューIDを取得
        if Cooks.exists():
            Cookid = Menucook.objects.filter(menu=Cooks[0]['menu_id']).values('cook')

            for i in range(len(Cookid)):
                # 料理の詳細情報を取得
                CookDetail = Cook.objects.filter(cook_id=Cookid[i]['cook']).values(
                    'cook_id', 'cookname', 'recipe_text', 'calorie', 'protein', 'lipids', 'carbohydrates', 'fiber', 'saltcontent'
                )
                choice_list = list(CookDetail.values())
                cooklist.append(choice_list[0])

                # 材料情報を取得
                materials = Recipe.objects.filter(cook=Cookid[i]['cook']).values('material', 'quantity')
                materialdetaillist = []
                for material in materials:
                    materialdetail = {}
                    material_info = Material.objects.filter(material_id=material['material']).values('name')
                    materialdetail['materialname'] = material_info[0]['name']
                    materialdetail['quantity'] = material['quantity']
                    materialdetaillist.append(materialdetail)

                materiallist.append(materialdetaillist)

                # 画像情報を取得
                cookimage = Cookimage.objects.filter(cook_id=Cookid[i]['cook']).values('image_id')
                if cookimage.exists():
                    image_id = cookimage[0]['image_id']
                    image_path = Image.objects.filter(image_id=image_id).values('image')[0]['image']
                    cooklist[-1]['image_path'] = image_path
                else:
                    cooklist[-1]['image_path'] = None
        else:
            # メニューがない場合はエラーハンドリングや適切な処理を追加することも検討
            logging.debug(f"No menu found for {currentday} and time {time}")

        return render(request, self.template_name, {
            'day': day,
            'time': time,
            'cook_list': cooklist,
            'material_list': json.dumps(materiallist)  # JSON形式で渡す
        })

class HealthSelectionView(TemplateView):
    template_name = 'health/health_selection.html'

    def get(self, request, *args, **kwargs):
        day_str = kwargs.get('day')  # URLからdayを取得
        year = datetime.now().year  # 現在の年を使う
        formatted_day_str = f"{year}-{day_str}"  # '2025-01-31' の形式に変換

        try:
            day = datetime.strptime(formatted_day_str, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponseBadRequest("無効な日付形式です。YYYY-MM-DD 形式にしてください。")

        # GETリクエストで選ばれた食事時間（デフォルトで朝にする）
        mealtime = request.session.get('mealtime', 0)

        # 指定された日付のmeal_dayの最大数を取得
        user = request.user
        existing_menus = Menu.objects.filter(user=user, meal_day=day)
        max_mealtime = existing_menus.aggregate(Max('mealtime'))['mealtime__max']

        # meal_dayが存在しない場合は朝から入力させる
        if max_mealtime is None:
            mealtime = 0
        # meal_dayの最大数が0の場合は昼から入力させる
        elif max_mealtime == 0:
            mealtime = 1
        # meal_dayの最大数が1の場合は晩から入力させる
        elif max_mealtime == 1:
            mealtime = 2
        # meal_dayの最大数が2の場合は朝から入力させる
        elif max_mealtime == 2:
            mealtime = 0

        # 食事時間に対応するメニューをフィルタリング
        form = CookSelectForm()
        form.fields['CookSelect'].queryset = Cook.objects.filter(type="1")

        context = {
            'day': day,
            'mealtime': mealtime,  # 選択された食事時間
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # セッションからmealtimeを取得
        mealtime = request.session.get('mealtime', 0)

        # 年齢で処理を変えるためのhandlers
        context = super().get_context_data(**kwargs)
        handlers = [
            ((1, 2), process_group_1_2),
            ((3, 5), process_group_3_5),
            ((6, 7), process_group_6_7),
            ((8, 9), process_group_8_9),
            ((10, 11), process_group_10_11),
            ((12, 14), process_group_12_14),
            ((15, 17), process_group_15_17),
            ((18, 29), process_group_18_29),
            ((30, 49), process_group_30_49),
            ((50, 64), process_group_50_64),
            ((65, 74), process_group_65_74),
            ((75, float('inf')), process_group_75_plus),
        ]

        # 入力されたformを取得
        form = CookSelectForm(request.POST)

        # ユーザの家族人数を数えるためのcount
        count = 1

        # もしformが正常に入力されていたら
        if form.is_valid():
            # 選択された料理名を取ってくる
            name = form.cleaned_data['CookSelect']

            # 料理の栄養情報を取ってくる
            cook = Cook.objects.filter(cookname=name).values('cook_id', 'calorie', 'protein', 'lipids', 'carbohydrates', 'fiber', 'saltcontent')

            # リストに入っている先頭のオブジェクトを取ってくる
            cookdata = cook[0]

            # ログイン中のユーザを代入
            user = request.user

            # 家族の必要栄養情報の初期値を代入
            family_calorie = 0
            family_protein = 0
            family_lipids = 0
            family_carbohydrates = 0
            family_fiber = 0
            family_saltcontent = 0

            # userの誕生日から年齢を計算
            birth_date = datetime.strptime(user.age, "%Y/%m/%d")
            today = datetime.today()
            age = today.year - birth_date.year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1

            for (start, end), handler in handlers:
                if start <= age <= end:
                    calorie, protein, libids, carbohydrates, fiber, saltcontent = handler(age, user.gender, float(user.weight))
                    break

            # 年齢から計算した必要栄養情報を家族の必要栄養情報に足す
            family_calorie += calorie
            family_protein += protein
            family_lipids += libids
            family_carbohydrates += carbohydrates
            family_fiber += fiber
            family_saltcontent += saltcontent

            # ユーザーの家族情報を取得
            userfamily = Familymember.objects.filter(user=user).order_by('family_id').values('family_id', 'family_gender', 'family_age', 'family_height', 'family_weight')

            # 家族の人数分ループ
            for i in userfamily:
                if 'family_id' not in i:  # family_id がない場合はスキップ
                    continue

                # user自身の分（最初のデータ）は栄養計算から省く
                if i['family_id'] == userfamily[0]['family_id']:
                    continue

                # 家族の年齢を取得
                family_age = datetime.strptime(i['family_age'], "%Y/%m/%d")
                today = datetime.today()
                family_age = today.year - family_age.year

                # 年齢をもとに必要栄養情報を取得
                for (start, end), handler in handlers:
                    if start <= family_age <= end:
                        calorie, protein, libids, carbohydrates, fiber, saltcontent = handler(family_age, i['family_gender'], float(i['family_weight']))
                        break

                    # 必要栄養情報を家族の必要栄養情報に足す
                    family_calorie += calorie
                    family_protein += protein
                    family_lipids += libids
                    family_carbohydrates += carbohydrates
                    family_fiber += fiber
                    family_saltcontent += saltcontent
                    count += 1  # 処理をした回数だけ家族の人数を増やす

            # 主菜の栄養情報を料理の栄養情報に足す
            all_calorie = count * cookdata['calorie']
            all_protein = count * cookdata['protein']
            all_libids = count * cookdata['lipids']
            all_carbohydrates = count * cookdata['carbohydrates']
            all_fiber = count * cookdata['fiber']
            all_saltcontent = count * cookdata['saltcontent']

            subcook = []

            # 家族の一食あたりの栄養必要量
            need_calorie = family_calorie / 3
            need_protein = family_protein / 3
            need_libids = family_lipids / 3
            need_carbohydrates = family_carbohydrates / 3
            need_fiber = family_fiber / 3
            need_saltcontent = family_saltcontent / 3

            # 不足栄養素を計算
            deficiency_calorie = need_calorie - all_calorie
            deficiency_protein = need_protein - all_protein
            deficiency_libids = need_libids - all_libids
            deficiency_carbohydrates = need_carbohydrates - all_carbohydrates
            deficiency_fiber = need_fiber - all_fiber
            deficiency_saltcontentr = need_saltcontent - all_saltcontent

            if deficiency_calorie > 0:
                results = Cook.objects.filter(
                    type__in=[2, 3],
                    calorie__lte=deficiency_calorie / 3,
                    protein__gte=deficiency_protein / 3,
                    saltcontent__lte=deficiency_saltcontentr / 3
                ).values('cook_id', 'calorie', 'protein', 'lipids', 'carbohydrates', 'fiber', 'saltcontent')

                if len(results) != 0:
                    random_number = random.randint(0, len(results) - 1)
                    randomcookdata = results[random_number]
                    all_calorie += count * randomcookdata['calorie']
                    all_protein += count * randomcookdata['protein']
                    all_libids += count * randomcookdata['lipids']
                    all_carbohydrates += count * randomcookdata['carbohydrates']
                    all_fiber += count * randomcookdata['fiber']
                    all_saltcontent += count * randomcookdata['saltcontent']
                    subcook.append(randomcookdata['cook_id'])

            # day は '01-01' のような形式で渡される
            day_str = self.kwargs.get('day')
            year = datetime.now().year  # 現在の年を使う
            formatted_day_str = f"{year}-{day_str}"  # '2025-01-31' の形式に変換
            day = datetime.strptime(formatted_day_str, "%Y-%m-%d").date()

            # 次の食事時間をセッションで管理
            next_mealtime = (mealtime + 1) % 3  # 0 -> 1 -> 2 -> 0に戻る
            request.session['mealtime'] = next_mealtime

            # 同じday, mealtimeのMenuが存在するか確認
            existing_menu = Menu.objects.filter(user=user, meal_day=day, mealtime=str(mealtime)).first()

            if not existing_menu:
                # Menuが存在しない場合は新規にMenuを作成
                menu = Menu(user=request.user, meal_day=day, mealtime=str(mealtime))
                menu.save()
            else:
                # Menuが存在する場合、そのmenu_idを使ってMenucookを削除
                menu = existing_menu

                # 既存のMenucookデータを削除（menu_idが一致するものを削除）
                Menucook.objects.filter(menu_id=menu.menu_id).delete()

            for i in range(len(subcook) + 1):
                if i == 0:
                    cook = Cook.objects.get(cook_id=cookdata['cook_id'])
                    menucook = Menucook(menu=menu, cook=cook)
                    menucook.save()
                else:
                    cook = Cook.objects.get(cook_id=subcook[i - 1])
                    menucook = Menucook(menu=menu, cook=cook)
                    menucook.save()

            # 最後の食事時間が選ばれたら完了
            if next_mealtime == 0:
                return redirect('health:health_selectioncomplate', day=day)
            else:
                # 食事時間に対応するメニューをフィルタリング
                form = CookSelectForm()
                form.fields['CookSelect'].queryset = Cook.objects.filter(type="1")
                return render(request, 'health/health_selection.html', {'mealtime': next_mealtime, 'day': day_str, 'form': form})

        else:
            return render(request, 'health/health_selection.html')



                
class HealthSelectionComplateView(TemplateView):
    template_name='health/health_selectioncomplate.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        day = self.kwargs.get('day')
        menu = Menu.objects.filter(user=request.user, meal_day=day).values("menu_id", "mealtime").order_by('mealtime')
        logging.debug(menu)
        breakfast = menu[0]
        lunch = menu[1]
        dinner = menu[2]
        breakfastimage = image_get(breakfast)
        lunchimage = image_get(lunch)
        dinnerimage = image_get(dinner)
            
            
            
        return render(request, self.template_name, {"breakfastimage":breakfastimage, "lunchimage":lunchimage,"dinnerimage":dinnerimage })
 



