from venv import logger
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import TemplateView
from administrator.models import Material, Image,CookImagesave
from .models import Userrecipe, Postimage, Bbs, Favorite
from .forms import RecipeAddForm, RecipeEditForm
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.db.models import Sum
import logging, os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
 
 
class BulletinBoardView(TemplateView):
    template_name = 'keijiban/BulletinBoard.html'
 
    def get(self, request, *args, **kwargs):
        user = self.request.user
        search_query = request.GET.get('search_query', '')  # 検索クエリを取得
 
        # 検索クエリが指定されている場合、Bbsモデルをフィルタリング
        if search_query:
            bbs = Bbs.objects.exclude(user_id=user.user_id).filter(name__icontains=search_query)
        else:
            bbs = Bbs.objects.exclude(user_id=user.user_id)  # 自分の投稿以外を表示
 
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
 
            is_favorite = Favorite.objects.filter(post=post, user=user, favorite_flag=True).exists()
 
            bbs_with_images.append({
                'post': post,
                'images': i,
                'is_favorite': is_favorite,  # お気に入り状態を追加
            })
 
        context = {
            'user': user,
            'bbs_with_images': bbs_with_images,  # 画像データを含むBbs情報
            'search_query': search_query,  # 検索クエリをコンテキストに含める
        }
 
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
 
            return redirect('bbs:PostsComplate', name=name)
       
        else:
            logging.debug('フォームが無効です: %s', form.errors)        
            return render(request, self.template_name)
 
class PostsComplateView(TemplateView):
    template_name = 'keijiban/toukou/posts_complate.html'

    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        try:
            post = Bbs.objects.get(name=name)  # name で投稿を取得
            post_title = post.name
            post_description = post.recipe_text
        except Bbs.DoesNotExist:
            post_title = "投稿が見つかりません"
            post_description = "該当するレシピが存在しません"

        context = {
            'post_title': post_title,
            'post_description': post_description,
        }

        return render(request, self.template_name, context)

 
def get_materials(request, materialname):
        logging.debug(materialname)
        logging.debug("げっとまてりある")
 
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
 
class MyBulletinBoardView(TemplateView):
    template_name = 'keijiban/syusai/myBulletinBoard.html'
 
    def get(self, request, *args, **kwargs):
        user = self.request.user
        search_query = request.GET.get('search_query', '')  # 検索クエリを取得
 
        # 検索クエリが指定されている場合、Bbsモデルをフィルタリング
        if search_query:
            bbs = Bbs.objects.filter(name__icontains=search_query, user=user)
        else:
            bbs = Bbs.objects.filter(user=user)  # ユーザーの投稿のみ表示
 
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
            'user': user,
            'bbs_with_images': bbs_with_images,  # 画像データを含むBbs情報
            'search_query': search_query,  # 検索クエリをコンテキストに含める
        }
 
        return self.render_to_response(context)
   
logger = logging.getLogger(__name__)

class EditView(View):
    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Bbs, post_id=post_id)

        # 投稿が現在のユーザーのものでなければアクセスを拒否
        if post.user != request.user:
            return redirect('bbs:MyBulletinBoard')  # 不正アクセス防止

        # 投稿内容をフォームに埋め込む
        form = RecipeEditForm(instance=post)

        # Postimageから画像を取得
        post_images = Postimage.objects.filter(post=post).values('image')
        images = [{'url': Image.objects.get(image_id=img['image']).image, 'id': img['image']} for img in post_images]
        logging.debug(images)

        # 画像URLをコンテキストに追加
        return render(request, 'keijiban/henshuu/edit.html', {
            'form': form,
            'post': post,
            'images': images  # 画像URLのリストをコンテキストに渡す
        })

    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Bbs, post_id=post_id)

        # 投稿が現在のユーザーのものでなければアクセスを拒否
        if post.user != request.user:
            return redirect('bbs:MyBulletinBoard')  # 不正アクセス防止

        form = RecipeEditForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()  # フォームのデータを保存（画像も含む）

            # 画像をPostimageテーブルに保存（必要に応じて追加）
            if 'image1' in request.FILES:
                image1_instance = Image(image=request.FILES['image1'])
                image1_instance.save()
                Postimage.objects.create(post=post, image=image1_instance)
            if 'image2' in request.FILES:
                image2_instance = Image(image=request.FILES['image2'])
                image2_instance.save()
                Postimage.objects.create(post=post, image=image2_instance)
            if 'image3' in request.FILES:
                image3_instance = Image(image=request.FILES['image3'])
                image3_instance.save()
                Postimage.objects.create(post=post, image=image3_instance)

            # 追加された画像を処理
            for file in request.FILES.getlist('additional_images'):
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(file.name, file)
                file_url = fs.url(filename)
                image_instance = Image(image=file_url)
                image_instance.save()
                Postimage.objects.create(post=post, image=image_instance)

            # 削除する画像を処理
            deleted_images = request.POST.get('deleted_images', '').split(',')
            for image_id in deleted_images:
                if image_id:
                    Postimage.objects.filter(post=post, image_id=image_id).delete()
                    Image.objects.filter(image_id=image_id).delete()

            return redirect('bbs:editcomplate')  # 編集後にeditcomplateにリダイレクト

        # エラーがある場合も画像を渡す
        post_images = Postimage.objects.filter(post=post).values('image')
        images = [{'url': Image.objects.get(image_id=img['image']).image, 'id': img['image']} for img in post_images]
        logging.debug(images)

        return render(request, 'keijiban/henshuu/edit.html', {'form': form, 'post': post, 'images': images})
    
class Editcomplate(TemplateView):
    template_name = 'keijiban/henshuu/editcomplate.html'

class DeleteView(TemplateView):
    template_name = 'keijiban/toukou/deleteconfirm.html'
 
    def get(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = get_object_or_404(Bbs, post_id=post_id)
        return self.render_to_response({'post': post})
 
    def post(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = get_object_or_404(Bbs, post_id=post_id)
 
        # 関連するPostimageデータを削除
        Postimage.objects.filter(post_id=post_id).delete()
 
        # Userrecipe の削除（もし関連している場合）
        Userrecipe.objects.filter(post_id=post_id).delete()
 
        # Bbsデータを削除
        post.delete()

        return redirect(reverse('bbs:PostsDeleteComplate'))
 
class DeleteComplateView(TemplateView):
    template_name = 'keijiban/toukou/deletecomplete.html'
 
class FavoriteView(TemplateView):
    template_name = 'keijiban/iine/favorite.html'
 
    def get(self, request, *args, **kwargs):
        user = self.request.user
        search_query = request.GET.get('search_query', '')  # 検索クエリを取得
       
        # お気に入りの投稿IDリストを取得
        favorite_post_ids = Favorite.objects.filter(user=user, favorite_flag=True).values_list('post_id', flat=True)
 
        # 検索クエリがある場合は名前でフィルタ、なければお気に入りの投稿をすべて取得
        if search_query:
            bbs_query = Bbs.objects.exclude(user_id=user.user_id).filter(name__icontains=search_query, post_id__in=favorite_post_ids)
        else:
            bbs_query = Bbs.objects.exclude(user_id=user.user_id).filter(post_id__in=favorite_post_ids)
 
        bbs_with_images = []
 
        # 各Bbsに関連する画像を取得
        for post in bbs_query:
            images = Postimage.objects.filter(post=post).values('image')  # Postimageから画像を取得
            logging.debug(images)
 
            # 画像がない場合はデフォルト画像を設定
            if images:
                img = images[0]
                imagepath = Image.objects.filter(image_id=img['image']).values('image').first()  # 最初の画像を取得
                logging.debug(imagepath)
 
                # 画像が見つかった場合
                if imagepath:
                    i = imagepath['image']
                else:
                    i = 'default_image_path.jpg'
            else:
                i = 'default_image_path.jpg'  # 投稿に画像がない場合はデフォルト画像を設定
 
            is_favorite = Favorite.objects.filter(post=post, user=user, favorite_flag=True).exists()
 
            bbs_with_images.append({
                'post': post,
                'images': i,
                'is_favorite': is_favorite,  # お気に入り状態を追加
            })
 
        context = {
            'user': user,
            'bbs_with_images': bbs_with_images,  # 画像データを含むBbs情報
            'search_query': search_query,  # 検索クエリをコンテキストに含める
        }
 
        return self.render_to_response(context)
 
   
class RankView(TemplateView):
    template_name = 'keijiban/iine/ranking.html'
 
    def get(self, request, *args, **kwargs):
        user = self.request.user
        search_query = request.GET.get('search_query', '')  # 検索クエリを取得
 
        # 各投稿のお気に入り数を集計して多い順に並べる
        bbs = Bbs.objects.annotate(total_likes=Sum('favorite__favorite_flag')).order_by('-total_likes')
 
        # 検索クエリがあればフィルタリングする
        if search_query:
            bbs = bbs.filter(name__icontains=search_query)
 
        bbs_with_images = []
 
        # 各Bbsに関連する画像を取得
        for post in bbs:
            images = Postimage.objects.filter(post=post).values('image')  # Postimageから画像を取得
            logging.debug(images)
 
            # 画像がない場合はデフォルト画像を設定
            if images:
                img = images[0]
                imagepath = Image.objects.filter(image_id=img['image']).values('image').first()  # 最初の画像を取得
                logging.debug(imagepath)
 
                # 画像が見つかった場合
                if imagepath:
                    i = imagepath['image']
                else:
                    i = 'default_image_path.jpg'
            else:
                i = 'default_image_path.jpg'  # 投稿に画像がない場合はデフォルト画像を設定
 
            is_favorite = Favorite.objects.filter(post=post, user=user, favorite_flag=True).exists()
            total_favorites = Favorite.objects.filter(post=post, favorite_flag=True).count()
 
            bbs_with_images.append({
                'post': post,
                'images': i,
                'is_favorite': is_favorite,  # お気に入り状態を追加
                'total_favorites': total_favorites,  # お気に入り数を追加
            })
 
        context = {
            'user': user,
            'bbs_with_images': bbs_with_images,  # 画像データを含むBbs情報
            'search_query': search_query,  # 検索クエリをコンテキストに含める
        }
 
        return self.render_to_response(context)
 
def toggle_favorite(request, post_id):
    user = request.user
    post = Bbs.objects.get(post_id=post_id)
 
    # お気に入りレコードがあるかどうかをチェック
    favorite_entry = Favorite.objects.filter(post=post, user=user).first()
 
    if favorite_entry:
        # 既にお気に入りに登録されている場合、flagを反転
        if favorite_entry.favorite_flag:
            favorite_entry.favorite_flag = False
            favorite_entry.save()
            return JsonResponse({'status': 'removed'})
        else:
            favorite_entry.favorite_flag = True
            favorite_entry.save()
            return JsonResponse({'status': 'added'})
    else:
        # まだお気に入りがない場合、新規作成
        Favorite.objects.create(post=post, user=user, favorite_flag=True)
        return JsonResponse({'status': 'added'})
    
class ShousaiView(TemplateView):
    template_name = 'keijiban/shousai/shousai.html'
 
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Bbs, post_id=post_id)
        images = Postimage.objects.filter(post=post).values('image')
 
        image_paths = []
        for img in images:
            imagepath = Image.objects.filter(image_id=img['image']).values('image')
            if imagepath:
                image_paths.append(imagepath[0]['image'])
            else:
                image_paths.append('default_image_path.jpg')
 
        context = {
            'post': post,
            'images': image_paths,
        }
        return render(request, self.template_name, context)