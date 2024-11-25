from django.urls import path, include
from . import  views
from .views import KazokuHenkoView


app_name = "cookapp"

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('Login1/', views.CustomLogin1View.as_view(), name='Login1'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('health_management_main/', views.HealthMainView.as_view(), name='health_management_main'),
    path('health_selection/', views.HealthSelectionView.as_view(), name='health_selection'),
    path('health_selectioncomplate/', views.HealthSelectionComplateView.as_view(), name='health_selectioncomplate'),
    path('health_menuconfirmation/', views.HealthMenuConfirmationView.as_view(), name='health_menuconfirmation'),
    path('setting/', views.SettingView.as_view(), name='setting'),
    path('acount_setting/', views.AcountSettingView.as_view(), name='acount_setting'),
    path('family_info/', views.FamilyInfoView.as_view(), name='family_info'),
    path('body_info_update/', views.BodyInfoUpdateView.as_view(), name='body_info_update'),
    path('body_info_ok/', views.BodyInfoOkView.as_view(), name='body_info_ok'),
    path('notification_setting/', views.NotificationSettingView.as_view(), name='notification_setting'),
    path('subscription_setting/', views.SubscriptionSettingView.as_view(), name='subscription_setting'),
    path('subscription_login/', views.SubscriptionLoginView.as_view(), name='subscription_login'),
    path('subscription_login_ok/', views.SubscriptionLoginOkView.as_view(), name='subscription_login_ok'),
    path('subscription_kaiyaku/', views.SubscriptionKaiyakuView.as_view(), name='subscription_kaiyaku'),
    path('subscription_kaiyaku_ok/', views.SubscriptionKaiyakuOkView.as_view(), name='subscription_kaiyaku_ok'),
    path('osirase/', views.OsiraseView.as_view(), name='osirase'),
    path('questions/', views.QuestionsView.as_view(), name='questions'),
    path('username/', views.UsernameView.as_view(), name='username'),
    path('username_henko_ok/', views.UsernameOkView.as_view(), name='username_henko_ok'),
    path('email/', views.EmailView.as_view(), name='email'),
    path('email_henko_ok/', views.EmailOkView.as_view(), name='email_henko_ok'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('password_henko_ok/', views.PasswordOkView.as_view(), name='password_henko_ok'),
    path('kazoku_add/', views.KazokuaddView.as_view(), name='kazoku_add'),
    path('kazoku_add_ok/', views.KazokuaddOkView.as_view(), name='kazoku_add_ok'),
    path('shokujirireki/', views. DietaryHistoryView.as_view(), name='dietaryhistory'),
    path('kazoku/henko/<int:family_id>/', KazokuHenkoView.as_view(), name='kazoku_henko'),
    path('kazoku_henko_ok/<int:family_id>/', views.KazokuHenkoOkView.as_view(), name='kazoku_henko_ok'),
    path('kazoku/kakunin/<int:family_id>/', views.KazokuKakuninView.as_view(), name='kazoku_kakunin'),
    path('health_graph/', views.HealthGraphView.as_view(), name='health_graph'),
    path('taikai/', views.confirm_taikai, name='confirm_taikai'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('kazoku_sakujo/', views.KazokuSakujoView.as_view(), name='kazoku_sakujo'),
]
