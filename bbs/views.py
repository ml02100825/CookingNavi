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
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Bbs
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import Bbs
from .forms import BbsForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Bbs, Postimage, Image
from django.contrib.auth.mixins import LoginRequiredMixin
import logging

logger = logging.getLogger(__name__)

class MyBulletinBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'keijiban/syusai/myBulletinBoard.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        search_query = request.GET.get('search_query', '')
        
        if search_query:
            # 検索クエリに一致する投稿をフィルタリング
            bbs = Bbs.objects.filter(name__icontains=search_query).exclude(user_id=user.user_id)
        else:
            # 最初は他のユーザーの投稿をフィルタリング
            bbs = Bbs.objects.exclude(user_id=user.user_id)

        bbs_with_images = []
        for post in bbs:
            # Postimage から対応する画像を取得
            postimages = Postimage.objects.filter(post_id=post.post_id)

            images = []
            for postimage in postimages:
                try:
                    image_obj = postimage.image  # Postimage に関連付けられた Image オブジェクト
                    images.append(image_obj.image)  # URL をリストに追加
                except AttributeError:
                    continue

            bbs_with_images.append({
                'post': post,
                'images': images
            })

        context = {
            'bbs_with_images': bbs_with_images,
            'show_my_posts': False,  # 自分の投稿を表示するかどうかのフラグ
            'search_query': search_query  # 検索クエリをコンテキストに追加
        }
        logger.debug("GET request: show_my_posts = False")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = request.user
        show_my_posts = request.POST.get('show_my_posts') == 'True'
        search_query = request.POST.get('search_query', '')
        
        logger.debug(f"POST request: show_my_posts = {show_my_posts}")

        if show_my_posts:
            # 自分が投稿したものをフィルタリング
            bbs = Bbs.objects.filter(user_id=user.user_id)
        else:
            if search_query:
                # 検索クエリに一致する投稿をフィルタリング
                bbs = Bbs.objects.filter(name__icontains=search_query).exclude(user_id=user.user_id)
            else:
                # 他のユーザーの投稿をフィルタリング
                bbs = Bbs.objects.exclude(user_id=user.user_id)

        bbs_with_images = []
        for post in bbs:
            # Postimage から対応する画像を取得
            postimages = Postimage.objects.filter(post_id=post.post_id)

            images = []
            for postimage in postimages:
                try:
                    image_obj = postimage.image  # Postimage に関連付けられた Image オブジェクト
                    images.append(image_obj.image)  # URL をリストに追加
                except AttributeError:
                    continue

            bbs_with_images.append({
                'post': post,
                'images': images
            })

        context = {
            'bbs_with_images': bbs_with_images,
            'show_my_posts': not show_my_posts,  # 自分の投稿を表示するかどうかのフラグを反転
            'search_query': search_query  # 検索クエリをコンテキストに追加
        }
        logger.debug(f"POST response: show_my_posts = {not show_my_posts}")
        return self.render_to_response(context)

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
                imageurl3 = Image(image = image3.image.url)
                imageurl3.save()
                bbsimage3 = Postimage(post = bbs, image = imageurl3)
                bbsimage3.save()
           
 
           
           
            for key in materials:
                material = Material.objects.get(material_id=key)
                recipe = Userrecipe(post = bbs, material = material ,quantity = materials[key])
                recipe.save()
            del request.session['materials']
            return redirect('bbs:PostsComplate')
        else:
            logging.debug('フォームが無効です: %s', form.errors)        
            return render(request, self.template_name)
        
class PostsComplateView(TemplateView):
    template_name = 'keijiban/toukou/posts_complate.html'

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

class EditView(DetailView):
    model = Bbs
    template_name = 'keijiban/henshuu/edit.html'
    context_object_name = 'bbs'

    def get_object(self, queryset=None):
        # URLの`post_id`から対象のBbsオブジェクトを取得
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Bbs, post_id=post_id)

    def get(self, request, *args, **kwargs):
        bbs = self.get_object()
        form = BbsForm(instance=bbs)

        # Bbsに関連付けられた画像を取得
        post_images = Postimage.objects.filter(post=bbs)
        images = [postimage.image.image.url for postimage in post_images]

        context = {
            'form': form,
            'bbs': bbs,
            'images': images,  # 画像のURLリスト
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bbs = self.get_object()
        form = BbsForm(request.POST, instance=bbs)

        if form.is_valid():
            form.save()  # フォームのデータを保存（更新）
            return redirect('bbs:MyBulletinBoard')  # 更新後にリダイレクト

        # エラーがある場合も画像を渡す
        post_images = Postimage.objects.filter(post=bbs)
        images = [postimage.image.image.url for postimage in post_images]

        return render(request, self.template_name, {
            'form': form,
            'bbs': bbs,
            'images': images,
        })