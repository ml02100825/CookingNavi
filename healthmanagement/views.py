import random
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
import urllib
from administrator.models import Cook, Cookimage, Image, Material, Recipe
from datetime import datetime, date, timedelta
from cookapp.models import Familymember
from .forms import CookSelectForm
from .models import Menu, Menucook
import json

import logging

def menu_exist(day):
    today = date.today()
    weekday = today.weekday()
    
    daydifference = weekday - day

    currentday = today + timedelta(days=-daydifference)
    menu = Menu.objects.filter(meal_day  = currentday)
    if menu:
        return "T"
    else:
        return "F"
    
def image_get(menu):
    menucook = Menucook.objects.filter(menu = menu['menu_id']).values('cook')
    for i in menucook:
        
        menuid = Cook.objects.filter(cook_id= i['cook']).values('cook_id', 'type')
        menuid = menuid[0]
        if menuid['type'] == '0':
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
        exist_list = []
        for i in range(7):
            
            result = menu_exist(i)
            exist_list.append(result)
            
        
        return render(request, self.template_name, {'exist_list': exist_list})

class HealthMenuView(TemplateView):
    template_name='health/health_menuconfirmation.html'
    
    def get(self, request, *args, **kwargs):
        cooklist = []
        materiallist = []
        materialdetaillist = []
        context = super().get_context_data(**kwargs)
        time = self.kwargs.get('time')
        day = self.kwargs.get('day')
        today = date.today()
        weekday = today.weekday()
        daydifference = weekday - day
        currentday = today + timedelta(days=-daydifference)
        Cooks = Menu.objects.filter(user=request.user,meal_day = currentday, mealtime = time).values('menu_id')
        Cookid = Menucook.objects.filter(menu =  Cooks[0]['menu_id']).values('cook')
        logging.debug(Cookid)
        for i in range(len(Cookid)):
            CookDetail = Cook.objects.filter(cook_id = Cookid[i]['cook']).values('cook_id','cookname','recipe_text','calorie','protein','lipids','carbohydrates','fiber','saltcontent')
            choice_list = list(CookDetail.values())
            cooklist.append(choice_list[0])
            materials = Recipe.objects.filter(cook = Cookid[i]['cook']).values('material','quantity')
            for j in range(len(materials)):
            
                choice_list = list(materials.values())
                materialdetail = {}
                material = Material.objects.filter(material_id = materials[j]['material']).values('name')
                materialdetail['materialname'] = material[0]['name']
                materialdetail['quantity'] = materials[j]['quantity']
                materialdetaillist.append(materialdetail)
                
            materiallist.append(materialdetaillist)
            materialdetaillist = []
            
        logging.debug(materiallist)
        CookDetail =CookDetail[0]
        
        logging.debug(cooklist)
        
        return render(request, self.template_name,{'cook_list': cooklist, 'material_list': materiallist})    

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
            mealtime = self.kwargs.get('mealtime')
            logging.debug("mealtime", mealtime)
            # 選択された料理名を取ってくる
            name = form.cleaned_data['CookSelect']
            logging.debug(name)
            # 料理の栄養情報を取ってくる
            cook = Cook.objects.filter(cookname = name).values('cook_id', 'calorie','protein','lipids','carbohydrates','fiber','saltcontent')
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

            subcook = []
            
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
            
            deficiency_calorie = need_calorie - all_calorie
            deficiency_protein = need_protein - all_protein
            deficiency_libids = need_libids - all_libids
            deficiency_carbohydrates = need_carbohydrates - all_carbohydrates
            deficiency_fiber = need_fiber - all_fiber
            deficiency_saltcontentr = need_saltcontent - all_saltcontent
            logging.debug("不足カロリー%f" , deficiency_calorie)
            logging.debug("不足タンパク質%f" ,deficiency_protein)
            logging.debug("不足脂質%f" , deficiency_libids)
            logging.debug("不足炭水化物%f" , deficiency_carbohydrates)
            logging.debug("不足食物繊維%f" , deficiency_fiber)
            logging.debug("不足塩分%f" , deficiency_saltcontentr)
            if need_calorie - all_calorie >0:
                results = Cook.objects.filter(
                type__in=[2, 3],
                calorie__lte=deficiency_calorie / 3,
                protein__gte=deficiency_protein / 3,
                saltcontent__lte=deficiency_saltcontentr / 3
                ).values('cook_id','calorie','protein','lipids','carbohydrates','fiber','saltcontent')
                logging.debug(results)
                logging.debug(len(results))
                if len(results) != 0:
                                
                    random_number = random.randint(0, len(results)-1)
                    randomcookdata =  results[random_number]
                    all_calorie += count * randomcookdata['calorie']
                    all_protein += count * randomcookdata['protein']
                    all_libids += count * randomcookdata['lipids']
                    all_carbohydrates += count * randomcookdata['carbohydrates']
                    all_fiber += count * randomcookdata['fiber']
                    all_saltcontent += count * randomcookdata['saltcontent']
                    subcook.append(randomcookdata['cook_id'])
                    logging.debug(results[random_number])
                    logging.debug(results[random_number])  
                    logging.debug("主菜のカロリー%f" , all_calorie)
                    logging.debug("主菜のタンパク質%f" , all_protein)
                    logging.debug("主菜の脂質%f" , all_libids)
                    logging.debug("主菜の炭水化物%f" , all_carbohydrates)
                    logging.debug("主菜の食物繊維%f" , all_fiber)
                    logging.debug("主菜の塩分%f" , all_saltcontent)
                    
                    if need_calorie - all_calorie >0:
                        while True:
                            # この無限ループ修正から
                            deficiency_calorie = need_calorie - all_calorie
                            deficiency_protein = need_protein - all_protein
                            deficiency_libids = need_libids - all_libids
                            deficiency_carbohydrates = need_carbohydrates - all_carbohydrates
                            deficiency_fiber = need_fiber - all_fiber
                            deficiency_saltcontentr = need_saltcontent - all_saltcontent
                            logging.debug("不足カロリー%f" , deficiency_calorie)
                            logging.debug("不足タンパク質%f" ,deficiency_protein)
                            logging.debug("不足脂質%f" , deficiency_libids)
                            logging.debug("不足炭水化物%f" , deficiency_carbohydrates)
                            logging.debug("不足食物繊維%f" , deficiency_fiber)
                            logging.debug("不足塩分%f" , deficiency_saltcontentr)
                            results = Cook.objects.filter(
                            type__in=[2, 3],
                            calorie__lte=deficiency_calorie / 3,
                            protein__gte=deficiency_protein / 3,
                            saltcontent__lte=deficiency_saltcontentr / 3
                            ).exclude(cook_id__in=subcook).values('cook_id','calorie','protein','lipids','carbohydrates','fiber','saltcontent')
                            logging.debug(len(results))
                            if len(results) == 0:
                                logging.debug("break")
                                break
                              
                            logging.debug(results)
                            logging.debug(len(results))
                            random_number = random.randint(0, len(results)-1)
                            randomcookdata =  results[random_number]
                            all_calorie += count * randomcookdata['calorie']
                            all_protein += count * randomcookdata['protein']
                            all_libids += count * randomcookdata['lipids']
                            all_carbohydrates += count * randomcookdata['carbohydrates']
                            all_fiber += count * randomcookdata['fiber']
                            all_saltcontent += count * randomcookdata['saltcontent']
                            subcook.append(randomcookdata['cookname'])
                            if need_calorie - all_calorie >0:
                                logging.debug("break")
                                break
                    #何が料理として使われるかチェックする
            logging.debug(subcook)
            today = date.today()
            weekday = today.weekday()
            context = super().get_context_data(**kwargs)
            day = self.kwargs.get('day') 
            daydifference = weekday - day

            currentday = today + timedelta(days=-daydifference)
            
            formatted_date  = currentday.strftime("%Y-%m-%d")
            logging.debug(formatted_date)
 
            menu =Menu(user = request.user, meal_day = formatted_date, mealtime = str(mealtime))
            menu.save()
            for i in range(len(subcook) + 1):
                if i == 0:
                    cook = Cook.objects.get(cook_id=cookdata['cook_id'])
                    menucook =  Menucook(menu =menu, cook =cook)
                    menucook.save()
                else:
                    cook = Cook.objects.get(cook_id =  subcook[i -1])
                    menucook = Menucook(menu =menu, cook = cook)
                    menucook.save()
            # url末尾に数字を追加。それで朝昼晩の判別を行う。献立が登録されたら次のページ(朝なら昼、昼なら晩)に飛ぶようにする
            # mealtimeをloggingでみてからmealtimeを増やして次のページに飛ばす処理を作る
            logging.debug(menu)

            new_mealtime = mealtime + 1
            logging.debug("mealtime", new_mealtime)
            context = {'mealtime':new_mealtime}
            if new_mealtime ==3:
                return redirect('health:health_selectioncomplate', day = formatted_date)
            return redirect('health:health_selection', day=day, mealtime=new_mealtime)
                
class HealthSelectionComplateView(TemplateView):
    template_name='health/health_selectioncomplate.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        day = self.kwargs.get('day')
        menu = Menu.objects.filter(user = request.user, meal_day = day).values("menu_id","mealtime").order_by('mealtime')
        logging.debug(menu)
        breakfast = menu[0]
        lunch = menu[1]
        dinner = menu[2]
        breakfastimage = image_get(breakfast)
        lunchimage = image_get(lunch)
        dinnerimage = image_get(dinner)
            
            
            
        return render(request, self.template_name, {"breakfastimage":breakfastimage, "lunchimage":lunchimage,"dinnerimage":dinnerimage })
 



