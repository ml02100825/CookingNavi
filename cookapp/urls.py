from django.urls import path
from . import  views

app_name = "cookapp"
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('Login1/', views.CustomLogin1View.as_view(), name='Login1'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('health_management_main/', views.HealthMainView.as_view(), name='health_management_main'),
    path('health_selection/', views.HealthSelectionView.as_view(), name='health_selection'),
    path('setting/', views.SettingView.as_view(), name='setting'),
    path('acount_setting/', views.AcountSettingView.as_view(), name='acount_setting'),
    path('family_info/', views.FamilyInfoView.as_view(), name='family_info'),
    path('body_info_update/', views.BodyInfoUpdateView.as_view(), name='body_info_update'),
    path('notification_setting/', views.NotificationSettingView.as_view(), name='notification_setting'),
    path('acount_setting/', views.AcountSettingView.as_view(), name='acount_setting'),
]