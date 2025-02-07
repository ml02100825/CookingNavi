import os
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from django.conf import settings
from cookapp.models import News  # 新しく作ったアプリのモデルをインポート
csv_file_path = os.path.join(os.path.dirname(__file__), "data", "news.csv")

with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print("カラム名:", reader.fieldnames)  # カラム名を出力
        News.objects.create(
            news_id=int(row["NEWS_ID"]),
            title=row["title"], 
            content=row["Content"],
            upload_time=row["UploadTime"],
            update_time=row["UpdateTime"],
            subscribe=row["Subscribe"],

        )

print("データの挿入が完了しました！")