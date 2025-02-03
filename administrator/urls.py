from django.urls import path
from . import views

app_name = "administrator"
urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('recipe/', views.RecipeView.as_view(), name='recipe'),
    path('recipe/add/', views.RecipeAddView.as_view(), name='recipeadd'),
    path('recipe/add/<int:material>/<int:materialamount>/', views.save_material, name='savematerial'),
    path('recipe/add/<str:materialname>/', views.get_materials, name='getmaterial'),
    path('recipe/add/done', views.RecipeAdd_doneView.as_view(), name='recipeadd_done'),
    path('bulletinboard2/', views.BulletinBoard2View.as_view(), name='BulletinBoard2'),
    path('recipe/edit/', views.RecipeEditView.as_view(), name='recipeedit'),
    path('deleteconfirm2/<int:post_id>/', views.DeleteConfirm2View.as_view(), name='delete_confirm2'),
]