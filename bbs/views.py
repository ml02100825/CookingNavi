from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.



class BulletinBoardView(TemplateView):
    template_name = 'keijiban/BulletinBoard.html'