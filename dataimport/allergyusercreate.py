
import os

from faker import Faker
import csv
import random
import django
import csv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),  "..")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cookingnavi.settings")  # プロジェクト名を適宜変更
django.setup()
from account.models import User, Userallergy
from cookapp.models import Familymember, Weight
fake = Faker('ja_JP')

allergys = ['1', '2', '3', '4', '5', '6', '7', '8'] #アレルギーのリスト
users = User.objects.all().values_list('user_id', flat=True)
userlist = list(users)
print(userlist)
for i in range(100):
    
    
    # 0 〜 3 の範囲でランダムな要素数を選択
    num_samples = random.randint(0, min(3, len(allergys)))

    # ランダムな個数の要素を取得
    allergy = random.sample(allergys, num_samples)
    print(allergy)
    user_id = random.choice(userlist)
    user = User.objects.get(user_id=user_id)
    if len(allergy) == 0:
        continue
    else:
        for i in range(len(allergy)):
            
            Userallergy.objects.create(
                user = user,
                allergy = allergy[i]
            )
    userlist.remove(user_id)
    
print("データの挿入が完了しました！")
    