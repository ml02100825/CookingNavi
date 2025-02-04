from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

from administrator.models import Recipe
from healthmanagement.models import Menu, Menucook
from .forms import DateRangeForm

class BuyListView(TemplateView):
    template_name = 'kaimonorisuto/buylist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DateRangeForm()  # フォームをコンテキストに追加
        return context

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # 指定された日付範囲に基づいてメニューを取得
            menus = Menu.objects.filter(meal_day__range=[start_date, end_date])
            
            # メニューに関連する料理を取得
            menu_cooks = Menucook.objects.filter(menu__in=menus)
            
            # 料理に関連する材料とその量を取得
            recipes = Recipe.objects.filter(cook__in=[mc.cook for mc in menu_cooks])
            
            # 材料ごとに量を集計
            material_quantities = {}
            for recipe in recipes:
                material_name = recipe.material.name
                if material_name in material_quantities:
                    material_quantities[material_name] += recipe.quantity
                else:
                    material_quantities[material_name] = recipe.quantity
            
            return render(request, self.template_name, {
                'form': form,
                'start_date': start_date,
                'end_date': end_date,
                'material_quantities': material_quantities,  # 材料とその量をコンテキストに追加
            })
        else:
            return render(request, self.template_name, {'form': form})
    