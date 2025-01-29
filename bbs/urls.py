from django.contrib import admin
from django.urls import path
from . import views
from .views import ShousaiView
 
 
app_name = "bbs"
 
urlpatterns = [
   
    path('BulletinBoard/', views.BulletinBoardView.as_view(), name='BulletinBoard'),
 
    path('Posts', views.PostsView.as_view(), name='Posts'),
    path('PostsComplate/<str:name>/', views.PostsComplateView.as_view(), name='PostsComplate'),
 
    path('Posts/<int:material>/<int:materialamount>/', views.save_material, name='savematerial'),
    path('Posts/<str:materialname>/', views.get_materials, name='getmaterial'),
   
    path('MyBulletinBoard/', views.MyBulletinBoardView.as_view(), name='MyBulletinBoard'),
    path('edit/<int:post_id>/', views.EditView.as_view(), name='edit'),
    path('editcomplate/', views.Editcomplate.as_view(), name='editcomplate'),
    path('bbs/delete/<int:post_id>/', views.DeleteView.as_view(), name='PostsDelete'),
    path('bbs/delete/', views.DeleteComplateView.as_view(), name='PostsDeleteComplate'),
 
    path('toggle_favorite/<int:post_id>/', views.toggle_favorite, name='toggle_favorite'),
   
    path('favorite/', views.FavoriteView.as_view(), name='favorite'),
    path('ranking/', views.RankView.as_view(), name='ranking'),
    
    path('shousai/<int:post_id>/', ShousaiView.as_view(), name='shousai'),
]