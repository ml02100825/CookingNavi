from django.contrib import admin
from django.urls import path
from . import views

app_name = "bbs"

urlpatterns = [
    
    path('Posts', views.PostsView.as_view(), name='Posts'),
    path('PostsComplate/', views.PostsComplateView.as_view(), name='PostsComplate'),
    path('edit/<int:post_id>/', views.EditView.as_view(), name='edit'),
    path('MyBulletinBoard/', views.MyBulletinBoardView.as_view(), name='MyBulletinBoard'),

    path('Posts/<int:material>/<int:materialamount>/', views.save_material, name='savematerial'),
    path('Posts/<str:materialname>/', views.get_materials, name='getmaterial'),
]