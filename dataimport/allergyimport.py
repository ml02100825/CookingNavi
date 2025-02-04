import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from cookapp.models import Allergy
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "allergy.csv")

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        Allergy.objects.create(
            allergy_id=int(row["ALLERGY_ID"]),
            material_id=row["MATERIAL_ID"], 
            allergy_category=row["ALLERGY_CATEGORY"],
            allergy_name=row["ALLERGY_NAME"],
        )

print("データの挿入が完了しました！")