from venv import logger
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from administrator.models import Cook
import datetime
from cookapp.models import Familymember
from .forms import CookSelectForm
from django.views.generic.edit import FormView

import logging

  
class HealthMainView(TemplateView):
    template_name='health/health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health/health_selection.html'
    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        weekday = today.weekday()
        context = super().get_context_data(**kwargs)
        day = self.kwargs.get('day') 
        daydifference = weekday - day

        currentday = today + datetime.timedelta(days=-daydifference)
        logging.debug(currentday)
        form = CookSelectForm()
        form.fields['CookSelect'].queryset = Cook.objects.filter(type="1")
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CookSelectForm(request.POST)
        if form.is_valid():
            user = request.user
            logging.debug(user.family)
            if user.family == True:
                family_calorie = 0
                family_protein = 0
                family_lipids = 0
                family_carbohydrates = 0
                family_fiber = 0
                family_saltcontent = 0
                userfamily = Familymember.objects.filter(user = user).values('family_gender','family_age','family_height','family_weight')
                logging.debug(userfamily)
                for i in userfamily:
                    
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
                    family_age = int(i['family_age'])  # 年齢の取得
                    Basal_metabolism = 0
                    for (start, end), handler in handlers:
                        if start <= family_age <= end:
                                Basal_metabolism =handler(family_age, i['family_gender'])
                                break
                    logging.debug(Basal_metabolism)
                    family_calorie += Basal_metabolism * float(i['family_weight'])
                    logging.debug(family_calorie)
                    logging.debug(i['family_gender'])
           
                
            return render(request, self.template_name, {'form': form})
                
class HealthSelectionComplateView(TemplateView):
    template_name='health/health_selectioncomplate.html'
 
class HealthMenuConfirmationView(TemplateView):
    template_name='health/health_menuconfirmation.html'
def process_group_1_2(age,gender):
    # 1-2歳の処理
    if gender == '0':
        Basal_metabolism = 61.0
    else:
        Basal_metabolism = 59.7
    return Basal_metabolism

def process_group_3_5(age,gender):
    # 3-5歳の処理
    if gender == '0':
        Basal_metabolism = 54.8
    else:
        Basal_metabolism = 52.2
        
    return Basal_metabolism


def process_group_6_7(age,gender):
    # 6-7歳の処理
    if gender == '0':
        Basal_metabolism = 44.3
    else:
        Basal_metabolism = 41.9
    return Basal_metabolism


def process_group_8_9(age,gender):
    # 8-9歳の処理
    if gender == '0':
        Basal_metabolism = 40.8
    else:
        Basal_metabolism = 38.3
    return Basal_metabolism


def process_group_10_11(age,gender):
    # 10-11歳の処理
    if gender == '0':
        Basal_metabolism = 37.4
    else:
        Basal_metabolism = 34.8
    return Basal_metabolism


def process_group_12_14(age,gender):
    # 12-14歳の処理
    if gender == '0':
        Basal_metabolism = 31.0
    else:
        Basal_metabolism = 29.6
    return Basal_metabolism

def process_group_15_17(age,gender):
    # 15-17歳の処理
    if gender == '0':
        Basal_metabolism = 27.0
    else:
        Basal_metabolism = 25.3
    return Basal_metabolism

def process_group_18_29(age,gender):
    # 18-29歳の処理
    if gender == '0':
        Basal_metabolism = 23.7
    else:
        Basal_metabolism = 22.1
    return Basal_metabolism

def process_group_30_49(age,gender):
    # 30-49歳の処理
    if gender == '0':
        Basal_metabolism = 22.5
    else:
        Basal_metabolism = 21.9
    return Basal_metabolism

def process_group_50_64(age,gender):
    # 50-64歳の処理
    if gender == '0':
        Basal_metabolism = 21.8
    else:
        Basal_metabolism = 20.7
    return Basal_metabolism

def process_group_65_74(age,gender):
    # 65-74歳の処理
    if gender == '0':
        Basal_metabolism = 21.6
    else:
        Basal_metabolism = 20.7
    return Basal_metabolism

def process_group_75_plus(age,gender):
    # 75歳以上の処理
    if gender == '0':
        Basal_metabolism = 21.5
    else:
        Basal_metabolism = 20.7
    return Basal_metabolism
 

