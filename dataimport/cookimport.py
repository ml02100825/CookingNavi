import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from administrator.models import Cook, Cookimage, Cookimagesave
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "cook.csv")
from administrator.models import Image
with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        Cook.objects.create(
            cook_id=int(row["Cook_ID"]),
            cookname=row["CookName"], 
            type=row["Type"],
            recipe_text=row["RECIPE_TEXT"],
            calorie=float(row["Calorie"]),
            protein=float(row["Protein"]),
            lipids=float(row["LIPIDS"]),
            carbohydrates=float(row["Carbohydrates"]),
            fiber=float(row["Fiber"]),
            saltcontent=float(row["SaltContent"]),
        )
        
imagecsv_file_path = os.path.join(os.path.dirname(__file__), "data", "image.csv")

with open(imagecsv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        Image.objects.create(
        image_id=int(row["Image_ID"]),
        image=row["Image"], 
    )
        


cookimagesavecsv_file_path = os.path.join(os.path.dirname(__file__), "data", "administrator_cookimagesave.csv")

with open(cookimagesavecsv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        Cookimagesave.objects.create(
            id=int(row["id"]),
            image=row["image"], 
            
        )
cookimagecsv_file_path = os.path.join(os.path.dirname(__file__), "data", "cookimage.csv")
with open(cookimagecsv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        cook = Cook.objects.get(cook_id=row["COOK_ID"])
        image = Image.objects.get(image_id=row["IMAGE_ID"])
        Cookimage.objects.create(
        cookimage_id=int(row["COOKIMAGE_ID"]),
        cook=cook, 
        image=image,
    )

print("データの挿入が完了しました！")