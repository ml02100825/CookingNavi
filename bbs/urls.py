from django.contrib import admin
from django.urls import path
from . import views

app_name = "bbs"

urlpatterns = [
    
    path('BulletinBoard/', views.BulletinBoardView.as_view(), name='BulletinBoard'),
    path('Posts/', views.PostsView.as_view(), name='Posts'),
]