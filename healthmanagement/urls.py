from django.contrib import admin
from django.urls import path
from . import views

app_name = "health"

urlpatterns = [
    path('health_management_main/', views.HealthMainView.as_view(), name='health_management_main'),
    path('health_selection/<int:day>', views.HealthSelectionView.as_view(), name='health_selection'),
    path('health_selectioncomplate/', views.HealthSelectionComplateView.as_view(), name='health_selectioncomplate'),
    path('health_menuconfirmation/', views.HealthMenuConfirmationView.as_view(), name='health_menuconfirmation'),
   
]