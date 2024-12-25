from venv import logger
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from administrator.models import Cook
import datetime

from .forms import CookSelectForm
from django.views.generic.edit import FormView

import logging

  
class HealthMainView(TemplateView):
    template_name='health/health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health/health_selection.html'
    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        weekday = today.weekday()
        context = super().get_context_data(**kwargs)
        day = self.kwargs.get('day') 
        daydifference = weekday - day

        currentday = today + datetime.timedelta(days=-daydifference)
        logging.debug(currentday)
        form = CookSelectForm()
        form.fields['CookSelect'].queryset = Cook.objects.filter(type="1")
        return render(request, self.template_name, {'form': form})
class HealthSelectionComplateView(TemplateView):
    template_name='health/health_selectioncomplate.html'
 
class HealthMenuConfirmationView(TemplateView):
    template_name='health/health_menuconfirmation.html'
 

