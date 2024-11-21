import logging
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from .forms import RecipeAddForm
from .models import Cook, Material



class HomeView(TemplateView):
    template_name='administrator/home/home.html'
class RecipeView(TemplateView):
    template_name = 'administrator/recipe/recipe.html'
class RecipeAddView(TemplateView):
    template_name = 'administrator/recipe/add/recipe_add.html'
    def get_materials(request, materialname):
        logging.debug(f"リクエストが来ました: {materialname}")
        materials = Material.objects.filter(name__icontains=materialname).values('Name')
        logging.debug("getmaterial")
        return JsonResponse(list(materials), safe=False)
    def get(self, request, *args, **kwargs):
        form = RecipeAddForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            materials = request.session.get('materials')
           
            # ユーザー作成
            cook_calorie = 0
            cook_protein = 0
            cook_lipids = 0
            cook_carbohydrates = 0
            cook_fiber = 0
            cook_saltcontent = 0
            name = form.cleaned_data['name']

            # フォームの入力内容でユーザーの詳細情報を更新
            type = form.cleaned_data['type']
            recipe_text = form.cleaned_data['recipe_text']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
          
            for i in range(len(materials)):
                material = materials[i]
                material_nutrition = Material.objects.filter(material_id=material).values('calorie','protein','lipids','fiber','carbohydrates','saltcontent')
                cook_calorie += material_nutrition[0]['calorie']
                cook_protein += material_nutrition[0]['protein']
                cook_lipids += material_nutrition[0]['lipids']
                cook_fiber += material_nutrition[0]['fiber']
                cook_carbohydrates += material_nutrition[0]['carbohydrates']
                cook_saltcontent += material_nutrition[0]['saltcontent']
            cook = Cook(cookname = name,type = type, recipe_text = recipe_text, age = cook_calorie, gender = cook_protein, height = cook_lipids,weight = cook_fiber,carbohydrates=cook_carbohydrates, saltcontent= cook_saltcontent)
            cook.save()
            
   
            return redirect('account:signup_completion')
        return render(request, self.template_name, {'form': form})
      

        return render(request, self.template_name)
def get_materials(request, materialname):
        logging.debug(materialname)
        logging.debug("げっとまてりある")
        
        materials = Material.objects.filter(name__icontains=materialname).values('material_id','name')
        logging.debug(materialname)
        logging.debug(materials)
        return JsonResponse(list(materials), safe=False)
def save_material(request, material):
        
      
            
        logging.debug("せーぶまてりある")
        logging.debug(material)
        materialname = Material.objects.filter(material_id = material).values('material_id','name')
    
        materialcheck = []
        materialcheck.append(materialname[0]['material_id'])
        logging.debug(request.session['materials'])
       # 'materials'がセッションに存在する場合
        if 'materials' in request.session:
            logging.debug(request.session['materials'],"セッション")
            materials = request.session['materials']
            if materials in materialcheck:
               logging.debug("削除")
               materials.remove(materialname[0]['material_id']) 
               request.session['materials'] = materials
               logging.debug("削除完了")
               logging.debug(request.session['materials'],"セッション")
               return JsonResponse(list(materialname), safe=False)

        else:
         # 存在しない場合は空リストを初期化
            materials = []
        material = materialname[0]['material_id']
        logging.debug(material)
        # materialnameがNoneでないことを確認してから、リストに追加
        if materialname:

            materials.append(material)

        # 更新したmaterialsリストをセッションに保存
        request.session['materials'] = materials
        return JsonResponse(list(materialname), safe=False)

    
