from django.shortcuts import render
from django.views.generic.base import TemplateView
from administrator.models import Cook
from datetime import datetime, date, timedelta
from cookapp.models import Familymember
from .forms import CookSelectForm

import logging

  
class HealthMainView(TemplateView):
    template_name='health/health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health/health_selection.html'
    def get(self, request, *args, **kwargs):
    
        today = date.today()
        weekday = today.weekday()
        context = super().get_context_data(**kwargs)
        day = self.kwargs.get('day') 
        daydifference = weekday - day

        currentday = today + timedelta(days=-daydifference)
        logging.debug(currentday)
        form = CookSelectForm()
        form.fields['CookSelect'].queryset = Cook.objects.filter(type="1")
        
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        # 年齢で処理を変えるためのhandlers
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
            logging.debug(name)
            # 料理の栄養情報を取ってくる
            cook = Cook.objects.filter(cookname = name).values('calorie','protein','lipids','carbohydrates','fiber','saltcontent')
            # リストに入っている先頭のオブジェクトを取ってくる
            cookdata = cook[0]
            logging.debug(cookdata)
            # ログイン中のユーザを代入
            user = request.user
            # 家族の必要栄養情報の初期値を代入
            family_calorie = 0
            family_protein = 0
            family_lipids = 0
            family_carbohydrates = 0
            family_fiber = 0
            family_saltcontent = 0
            logging.debug(user.family)
            # userの誕生日から年齢を計算
            birth_date = datetime.strptime(user.age, "%Y/%m/%d")

            # 現在の日付を取得
            today = datetime.today()

            # 年齢を計算
            age = today.year - birth_date.year

            # 生年月日がまだ来ていない場合は1歳引く
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1
            for (start, end), handler in handlers:
                if start <= age <= end:
                    calorie, protein, libids, carbohydrates, fiber, saltcontent =handler(age, user.gender, float(user.weight))
                    break
            # 年齢から計算した必要栄養情報を家族の必要栄養情報に足す
            family_calorie += calorie
            family_protein += protein
            family_lipids += libids
            family_carbohydrates += carbohydrates
            family_fiber += fiber
            family_saltcontent += saltcontent
            # もしユーザの家族フラグがTrueなら
            if user.family == True:

                
                #ログインしているuserの家族情報を取ってくる
                userfamily = Familymember.objects.filter(user = user).values('family_gender','family_age','family_height','family_weight')
                logging.debug(userfamily)
                # 家族の人数分ループ
                for i in userfamily:
                    # 家族の年齢を取得
                    family_age = int(i['family_age'])  # 年齢の取得
                    # 年齢をもとに必要栄養情報を取得
                    for (start, end), handler in handlers:
                        if start <= family_age <= end:
                                calorie, protein, libids, carbohydrates, fiber, saltcontent =handler(family_age, i['family_gender'], float(i['family_weight']))
                                break
                    # 必要栄養情報を家族の必要栄養情報に足す
                    family_calorie += calorie
                    family_protein += protein
                    family_lipids += libids
                    family_carbohydrates += carbohydrates
                    family_fiber += fiber
                    family_saltcontent += saltcontent
                    logging.debug(family_calorie)
                    logging.debug(family_protein)
                    logging.debug(family_lipids)
                    logging.debug(family_carbohydrates)
                    logging.debug(family_fiber)
                    logging.debug(family_saltcontent)
                    logging.debug(i['family_gender'])
                    # 処理をした回数だけ家族の人数を増やす
                    count +=1
            # 主菜の栄養情報を料理の栄養情報に足す
            all_calorie = count * cookdata['calorie']
            all_protein = count * cookdata['protein']
            all_libids = count * cookdata['lipids']
            all_carbohydrates = count * cookdata['carbohydrates']
            all_fiber = count * cookdata['fiber']
            all_saltcontent = count * cookdata['saltcontent']
            
            # 家族の一食あたりの栄養必要量 
            need_calorie = family_calorie / 3
            need_protein = family_protein / 3
            need_libids = family_lipids / 3
            need_carbohydrates = family_carbohydrates / 3
            need_fiber = family_fiber / 3
            need_saltcontent = family_saltcontent / 3        
            logging.debug("主菜のカロリー%f" , all_calorie)
            logging.debug("主菜のタンパク質%f" , all_protein)
            logging.debug("主菜の脂質%f" , all_libids)
            logging.debug("主菜の炭水化物%f" , all_carbohydrates)
            logging.debug("主菜の食物繊維%f" , all_fiber)
            logging.debug("主菜の塩分%f" , all_saltcontent)
            
            logging.debug("必要カロリー%f" , need_calorie)
            logging.debug("必要タンパク質%f" ,need_protein)
            logging.debug("必要脂質%f" , need_libids)
            logging.debug("必要炭水化物%f" , need_carbohydrates)
            logging.debug("必要食物繊維%f" , need_fiber)
            logging.debug("必要塩分%f" , need_saltcontent)
            return render(request, self.template_name, {'form': form})
                
class HealthSelectionComplateView(TemplateView):
    template_name='health/health_selectioncomplate.html'
 
class HealthMenuConfirmationView(TemplateView):
    template_name='health/health_menuconfirmation.html'
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
 

