import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from cookapp.models import Question  
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "question.csv")

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        Question.objects.create(
            question_id=int(row["Qustion_ID"]),
            question=row["Qustion"], 
            answer=row["Answer"]

        )

print("データの挿入が完了しました！")