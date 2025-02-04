import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.views.generic.base import TemplateView

from bbs.models import Bbs, Favorite, Postimage, Userrecipe
from .forms import RecipeAddForm
from .models import Cook, Material, Image,Cookimage,Recipe,AdministratorCookimagesave



class HomeView(TemplateView):
    template_name='administrator/home/home.html'
class RecipeView(TemplateView):
    template_name = 'administrator/recipe/recipe.html'
class RecipeAdd_doneView(TemplateView):
    template_name = 'administrator/recipe/add/recipe_add_completion.html'    
class RecipeAddView(TemplateView):
    template_name = 'administrator/recipe/add/recipe_add.html'

    def get(self, request, *args, **kwargs):
        form = RecipeAddForm()
        
      
        request.session['materials'] = {}
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = RecipeAddForm(request.POST, request.FILES)
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
          
            for key in materials:
                material = key
                value = materials[key] / 100
                material_nutrition = Material.objects.filter(material_id=material).values('calorie','protein','lipids','fiber','carbohydrates','saltcontent')
                if material_nutrition[0]['calorie'] != "-" and material_nutrition[0]['calorie']  != 'Tr' and material_nutrition[0]['calorie']  != '(Tr)':
                    cook_calorie += float(material_nutrition[0]['calorie']) * value
                if material_nutrition[0]['protein'] != "-" and material_nutrition[0]['protein']  != 'Tr'and material_nutrition[0]['protein']  != '(Tr)':    
                    cook_protein += float(material_nutrition[0]['protein']) * value
                if material_nutrition[0]['lipids'] != "-" and material_nutrition[0]['lipids']  != 'Tr'and material_nutrition[0]['lipids']  != '(Tr)':    
                   cook_lipids += float(material_nutrition[0]['lipids']) * value
                if material_nutrition[0]['fiber'] != "-" and material_nutrition[0]['fiber']  != 'Tr' and material_nutrition[0]['fiber']  != '(Tr)':       
                    cook_fiber += float(material_nutrition[0]['fiber'])* value
                if material_nutrition[0]['carbohydrates'] != "-"and material_nutrition[0]['carbohydrates']  != 'Tr'and material_nutrition[0]['carbohydrates']  != '(Tr)':   
                    cook_carbohydrates += float(material_nutrition[0]['carbohydrates']) * value
                if material_nutrition[0]['saltcontent'] != "-"and material_nutrition[0]['saltcontent']  != 'Tr'and material_nutrition[0]['saltcontent']  != '(Tr)':   
                    cook_saltcontent += float(material_nutrition[0]['saltcontent'])* value
            cook = Cook(cookname = name,type = type, recipe_text = recipe_text, calorie = cook_calorie, protein = cook_protein, lipids = cook_lipids,fiber = cook_fiber,carbohydrates=cook_carbohydrates, saltcontent= cook_saltcontent)
            cook.save()
            
            image1 = AdministratorCookimagesave(image = image1)
            image1.save()
            imageurl1 = Image(image = image1.image.url)
            imageurl1.save()
            cookimage1 = Cookimage(cook = cook, image = imageurl1)
            cookimage1.save()
           
            if image2 != None:
                image2 = AdministratorCookimagesave(image = image2)
                image2.save()
                imageurl2 = Image(image = image2.image.url)
                imageurl2.save()
                cookimage2 = Cookimage(cook = cook, image = imageurl2)
                cookimage2.save()
            if image3 != None:
                image3 = AdministratorCookimagesave(image = image3)
                image3.save()
                imageurl3 = Image(image = image3.image.url)
                imageurl3.save()
                cookimage3 = Cookimage(cook = cook, image = imageurl3)
                cookimage3.save()
            

            
            logging.debug(materials)
            for key in materials:
                material = Material.objects.get(material_id=key)
                recipe = Recipe(cook = cook, material = material,quantity = materials[key])
                recipe.save()
            

            
            del request.session['materials']
            return redirect('administrator:recipeadd_done')
        else:
         
            logging.debug('フォームが無効です: %s', form.errors)        
            return render(request, self.template_name)
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
        logging.debug(materialamount)
        materialname = Material.objects.filter(material_id = material).values('material_id','name')
       # 'materials'がセッションに存在する場合
        if 'materials' in request.session:
            logging.debug('セッションが存在する')
            materials = request.session['materials']
            logging.debug(materials)
            logging.debug(materialname[0]['material_id'] )
            if str(materialname[0]['material_id']) in materials:
               id = str(materialname[0]['material_id'])
               logging.debug(materials)
               del materials[id]
               logging.debug(materials)
               logging.debug(material)
               del request.session['materials']

               request.session['materials'] = materials
               logging.debug("削除完了")
            #    logging.debug(request.session['materials'],"セッション")
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
        print("セッションに保存されたデータ:", request.session['materials'])  # 確認用
        return JsonResponse(materials, safe=False)


class BulletinBoard2View(TemplateView):
    template_name = 'administrator/keijiban/BulletinBoard2.html'
 
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search_query', '')  # 検索クエリを取得
 
        # 検索クエリが指定されている場合、Bbsモデルをフィルタリング
        if search_query:
            bbs = Bbs.objects.filter(name__icontains=search_query)
        else:
            bbs = Bbs.objects.all()  # すべての投稿を表示
 
        bbs_with_images = []
 
        # 各Bbsに関連する画像を取得
        for post in bbs:
            images = Postimage.objects.filter(post=post).values('image')  # Postimageから画像を取得
            logging.debug(images)
 
            # 画像がない場合はスキップまたはデフォルト画像を使用
            if images:
                img = images[0]
                imagepath = Image.objects.filter(image_id=img['image']).values('image')
                logging.debug(imagepath)
 
                # 画像が見つかった場合
                if imagepath:
                    image = imagepath[0]
                    i = image['image']  # 画像パスを取得
                else:
                    i = 'default_image_path.jpg'  # 画像がない場合はデフォルト画像を設定
            else:
                i = 'default_image_path.jpg'  # 投稿に画像がない場合はデフォルト画像を設定
 
            bbs_with_images.append({
                'post': post,
                'images': i
            })
 
        context = {
            'bbs_with_images': bbs_with_images,  # 画像データを含むBbs情報
            'search_query': search_query,  # 検索クエリをコンテキストに含める
        }
 
        return self.render_to_response(context)

class DeleteConfirm2View(TemplateView):
    template_name = 'administrator/keijiban/deleteconfirm2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Bbs, pk=post_id)
        context['post'] = post
        return context

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Bbs, pk=post_id)
        
        # 関連するfavoriteテーブルのレコードを削除
        Favorite.objects.filter(post=post).delete()
        
        # 関連するuserrecipeテーブルのレコードを削除
        Userrecipe.objects.filter(post=post).delete()
        
        # 関連するpostimageテーブルのレコードと画像を削除
        post_images = Postimage.objects.filter(post=post)
        for post_image in post_images:
            image = get_object_or_404(Image, pk=post_image.image.image_id)
            post_image.delete()  # postimageレコードを先に削除
            image.delete()  # その後にimageレコードを削除
        
        # bbsテーブルのレコードを削除
        post.delete()
        
        return redirect('administrator:deletecomplete2')
    
class DeleteComplete2View(TemplateView):
    template_name = 'administrator/keijiban/deletecomplete2.html'

class RecipeEditView(TemplateView):
    template_name = 'administrator/recipe/edit/recipe_edit.html'

    def get(self, request, *args, **kwargs):
        # Cookテーブルから必要なデータを取得
        cooks = Cook.objects.values_list('cookname', flat=True)
        return render(request, 'administrator/recipe/edit/recipe_edit.html', {'cooks': cooks})
    