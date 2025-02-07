from django.urls import path
from . import views

app_name = "health"

urlpatterns = [
    path('health_management_main/', views.HealthMainView.as_view(), name='health_management_main'),
    path('health_selection/<str:day>/', views.HealthSelectionView.as_view(), name='health_selection'),
    path('health_selectioncomplate/<str:day>/', views.HealthSelectionComplateView.as_view(), name='health_selectioncomplate'),
    path('health_menu/<int:time>/<str:day>', views.HealthMenuView.as_view(), name='health_menu'),
]