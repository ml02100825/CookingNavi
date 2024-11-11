from django.urls import path
from . import  views

app_name = "cookapp"
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('health_management_main/', views.HealthMainView.as_view(), name='health_management_main'),
    path('health_selection/', views.HealthSelectionView.as_view(), name='health_selection')
]