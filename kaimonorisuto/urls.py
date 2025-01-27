from django.urls import path
from kaimonorisuto.views import BuyListView

app_name = "buylist"

urlpatterns = [
    path('kaimonorisuto/', BuyListView.as_view(), name='buylist'),
]
