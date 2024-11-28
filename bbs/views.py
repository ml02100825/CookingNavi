from venv import logger
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from administrator.models import Material, Image,CookImagesave
from .models import Userrecipe, Postimage,Bbs
from .forms import RecipeAddForm
from django.views.generic.edit import FormView
from django.views import View
import logging
# Create your views here.



class BulletinBoardView(TemplateView):
    template_name = 'keijiban/BulletinBoard.html'

class PostsView(TemplateView):
    template_name = 'keijiban/toukou/posts.html'
    def get(self, request, *args, **kwargs):
        logger.info(f"HTTP method: {request.method}")  # ログでリクエストのメソッドを確認
        form = RecipeAddForm()  # フォームクラスを設定
        
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        logger.info(f"HTTP method: {request.method}")  # ログでリクエストのメソッドを確認
        form = RecipeAddForm(request.POST, request.FILES)
        if form.is_valid():
            materials = request.session.get('materials')
           
            # ユーザー作成
            bbs_calorie = 0
            bbs_protein = 0
            bbs_lipids = 0
            bbs_carbohydrates = 0
            bbs_fiber = 0
            bbs_saltcontent = 0
            name = form.cleaned_data['name']

            # フォームの入力内容でユーザーの詳細情報を更新
            recipe_text = form.cleaned_data['recipe_text']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
          
            for key in materials:
                material = key
                value = materials[key] / 100
                material_nutrition = Material.objects.filter(material_id=material).values('calorie','protein','lipids','fiber','carbohydrates','saltcontent')
                if material_nutrition[0]['calorie'] != "-" and material_nutrition[0]['calorie']  != 'Tr'and material_nutrition[0]['calorie']  != '(Tr)':
                    bbs_calorie += float(material_nutrition[0]['calorie']) * value
                if material_nutrition[0]['protein'] != "-" and material_nutrition[0]['protein']  != 'Tr'and material_nutrition[0]['protein']  != '(Tr)':    
                    bbs_protein += float(material_nutrition[0]['protein']) * value
                if material_nutrition[0]['lipids'] != "-" and material_nutrition[0]['lipids']  != 'Tr'and material_nutrition[0]['lipids']  != '(Tr)':  
                   bbs_lipids += float(material_nutrition[0]['lipids']) * value
                if material_nutrition[0]['fiber'] != "-" and material_nutrition[0]['fiber']  != 'Tr'and material_nutrition[0]['fiber']  != '(Tr)':     
                    bbs_fiber += float(material_nutrition[0]['fiber'])* value
                if material_nutrition[0]['carbohydrates'] != "-"and material_nutrition[0]['carbohydrates']  != 'Tr' and material_nutrition[0]['carbohydrates']  != '(Tr)':   
                    bbs_carbohydrates += float(material_nutrition[0]['carbohydrates']) * value
                if material_nutrition[0]['saltcontent'] != "-"and material_nutrition[0]['saltcontent']  != 'Tr'and material_nutrition[0]['saltcontent']  != '(Tr)':   
                    bbs_saltcontent += float(material_nutrition[0]['saltcontent'])* value
            user = request.user
            bbs = Bbs(user =user,name = name, recipe_text = recipe_text, calorie = bbs_calorie, protein = bbs_protein, lipids = bbs_lipids,fiber = bbs_fiber,carbohydrates=bbs_carbohydrates, saltcontent= bbs_saltcontent)
            bbs.save()
            
            image1 = CookImagesave(image = image1)
            image1.save()
            imageurl1 = Image(image = image1.image.url)
            imageurl1.save()
            bbsimage1 = Postimage(post = bbs, image = imageurl1)
            bbsimage1.save()
           
            if image2 != None:
                image2 = CookImagesave(image = image2)
                image2.save()
                imageurl2 = Image(image = image2.image.url)
                imageurl2.save()
                bbsimage2 = Postimage(post = bbs, image = imageurl2)
                bbsimage2.save()
            if image3 != None:
                image3 = CookImagesave(image = image3)
                image3.save()
                imageurl3 = Image(image = image1.image.url)
                imageurl3.save()
                bbsimage3 = Postimage(post = bbs, image = imageurl3)
                bbsimage3.save()
            

            
            
            for key in materials:
                material = Material.objects.get(material_id=key)
                recipe = Userrecipe(post = bbs, material = material ,quantity = materials[key])
                recipe.save()
            

            
            del request.session['materials']
            return redirect('administrator:recipeadd_done')
        else:
         
            logging.debug('フォームが無効です: %s', form.errors)        
            return render(request, self.template_name)





class PostsComplateView(TemplateView):
    template_name = 'keijiban/toukou/posts_compate.html'

def get_materials(request, materialname):
        logging.debug(materialname)
        logging.debug("げっとまてりある")
        # materials = request.session['materials']

        # del request.session['materials']

        materials = Material.objects.filter(name__icontains=materialname).values('material_id','name')
        
        logging.debug(materialname)
        logging.debug(materials)
        return JsonResponse(list(materials), safe=False)
def save_material(request, material,materialamount):
            
        logging.debug("せーぶまてりある")
        logging.debug(material)
        materialname = Material.objects.filter(material_id = material).values('material_id','name')
       # 'materials'がセッションに存在する場合
        if 'materials' in request.session:
            
            materials = request.session['materials']
            logging.debug(materials)
            logging.debug(materialname[0]['material_id'] )
            if str(materialname[0]['material_id']) in materials:
               id = str(materialname[0]['material_id'])
               logging.debug(materials)
               del materials[id]
               logging.debug(materials)
               del request.session['materials']

               request.session['materials'] = materials
               logging.debug("削除完了")
               logging.debug(request.session['materials'],"セッション")
               return JsonResponse(materials, safe=False)

        else:
         # 存在しない場合は空リストを初期化
            materials = {}
        material = materialname[0]['material_id']
        logging.debug(material)
        # materialnameがNoneでないことを確認してから、リストに追加
        if materialname:

            materials[material] = materialamount

        # 更新したmaterialsリストをセッションに保存
        request.session['materials'] = materials
        return JsonResponse(materials, safe=False)
