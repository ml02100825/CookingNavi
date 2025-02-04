import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from administrator.models import Material  # 新しく作ったアプリのモデルをインポート
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "syokuhinclean.csv")

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        Material.objects.create(
            material_id=int(row["Material_ID"]),
            name=row["Name"], 
            calorie=row["Calorie"],
            protein=row["Protein"],
            lipids=row["Lipids"],
            fiber=row["Fiber"],
            carbohydrates=row["Carbohydrates"],
            saltcontent=row["SaltContent"],
        )

print("データの挿入が完了しました！")