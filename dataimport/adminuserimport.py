import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from account.models import User
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "user.csv")

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        User.objects.create(
            user_id=int(row["User_ID"]),
            name=row["Name"], 
            password=row["Password"],
            email=row["email"],
            gender=row["Gender"],
            age=row["Age"],
            height=float(row["Height"]),
            weight=float(row["Weight"]),
            is_superuser=row["is_superuser"],
            is_staff=row["is_staff"],
            family=row["Family"],
            last_login=row["last_login"],
            deleteflag=row["DeleteFlag"],
            subscribeflag=row["SubscribeFlag"],
            subjoin=row["SubJoin"],
            unsub=row["UnSub"],
            is_active=row["is_active"],
            date_joined=row["date_joined"],
            
        
        )
            
        

print("データの挿入が完了しました！")