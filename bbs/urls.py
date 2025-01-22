from django.urls import path
from . import views

app_name = "bbs"

urlpatterns = [
    
    path('Posts', views.PostsView.as_view(), name='Posts'),
    path('PostsComplate/', views.PostsComplateView.as_view(), name='PostsComplate'),
    path('edit/<int:post_id>/', views.EditView.as_view(), name='edit'),
    path('bbs/delete/<int:post_id>/', views.DeleteView.as_view(), name='PostsDelete'),
    path('deletecomplete/', views.DeleteCompleteView.as_view(), name='PostsDeleteComplete'),
    path('MyBulletinBoard/', views.MyBulletinBoardView.as_view(), name='MyBulletinBoard'),
    path('toggle_favorite/<int:post_id>/', views.FavoriteView.as_view(), name='toggle_favorite'),
    path('Posts/<int:material>/<int:materialamount>/', views.save_material, name='savematerial'),
    path('Posts/<str:materialname>/', views.get_materials, name='getmaterial'),
]