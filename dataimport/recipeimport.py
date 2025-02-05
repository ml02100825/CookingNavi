import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from administrator.models import Cook, Material, Recipe  # 新しく作ったアプリのモデルをインポート
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "recipe.csv")

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        cook = Cook.objects.get(cook_id=row["COOK_ID"])
        material = Material.objects.get(material_id=row["MATERIAL_ID"])
        print(cook)
        print("マテリアル",material)
        Recipe.objects.create(
            recipe_id=int(row["RECIPE_ID"]),
            cook=cook, 
            material=material,  
            quantity=int(row["material_quantity"]),
            
        )

print("データの挿入が完了しました！")