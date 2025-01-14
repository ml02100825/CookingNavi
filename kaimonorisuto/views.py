from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from .forms import DateRangeForm

class BuyListView(TemplateView):
    template_name = 'kaimonorisuto/buylist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DateRangeForm()  # フォームをコンテキストに追加
        return context

    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # ここでフォームに入力された日付を使って必要な処理を行う
            # 例: データベースからデータを取得して表示するなど
            
            return render(request, self.template_name, {
                'form': form,
                'start_date': start_date,
                'end_date': end_date,
                # 必要なら他のデータも返す
            })
        else:
            return render(request, self.template_name, {'form': form})

    