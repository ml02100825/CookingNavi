from django.contrib import admin
from django.urls import path
from . import views

app_name = "bbs"

urlpatterns = [
    
    path('BulletinBoard/', views.BulletinBoardView.as_view(), name='BulletinBoard'),
    path('Posts', views.PostsView.as_view(), name='Posts'),
    path('PostsComplate/', views.PostsComplateView.as_view(), name='PostsComplate'),

    path('Posts/<int:material>/<int:materialamount>/', views.save_material, name='savematerial'),
    path('Posts/<str:materialname>/', views.get_materials, name='getmaterial'),
]