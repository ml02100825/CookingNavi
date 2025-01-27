from django.urls import path, include
from . import views
from .views import KazokuHenkoView
from .views import KiyakuView
from django.contrib.auth import views as auth_views
from .views import password_reset_done_view

app_name = "cookapp"

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('Login1/', views.CustomLogin1View.as_view(), name='Login1'),
    path('home/', views.HomeView.as_view(), name='home'),
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
    path('shokujirireki/', views.DietaryHistoryView.as_view(), name='dietaryhistory'),
    path('kazoku/henko/<int:family_id>/', KazokuHenkoView.as_view(), name='kazoku_henko'),
    path('kazoku_henko_ok/<int:family_id>/', views.KazokuHenkoOkView.as_view(), name='kazoku_henko_ok'),
    path('kazoku/kakunin/<int:family_id>/', views.KazokuKakuninView.as_view(), name='kazoku_kakunin'),
    path('health_graph/', views.HealthGraphView.as_view(), name='health_graph'),
    path('confirm_taikai/', views.confirm_taikai, name='confirm_taikai'),
    path('taikai_ok/', views.taikai_ok, name='taikai_ok'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('kazoku/sakujo/<int:family_id>/', views.KazokuSakujoView.as_view(), name='kazoku_sakujo'),
    path('kazoku_sakujo_ok/<int:family_id>/', views.KazokuSakujoOkView.as_view(), name='kazoku_sakujo_ok'),
    path('kiyaku/', views.KiyakuView.as_view(), name='kiyaku'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='/password_reset/done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
]
