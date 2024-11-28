from venv import logger
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from administrator.models import Cook

from .forms import CookSelectForm
from django.views.generic.edit import FormView

import logging
# Create your views here.



class BulletinBoardView(TemplateView):
    template_name = 'keijiban/BulletinBoard.html'
    def get(self, request, *args, **kwargs):
        form = CookSelectForm()
        form.fields['CookSelect'] = Cook.objects.filter(type="1").values('id','name')
        return render(request, self.template_name, {'form': form})
  


