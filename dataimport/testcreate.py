
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
from account.models import User
from cookapp.models import Familymember, Weight
fake = Faker('ja_JP')
users = User.objects.all().values_list('user_id', flat=True)
userlist = list(users)
print(users)

for i in range(100):
    familiyname = fake.name()
    familygender = random.choice(['0', '1'])
    familyage = fake.date_of_birth(minimum_age=18, maximum_age=75)
    familyheight = random.uniform(150, 190)
    familyweight = random.uniform(50, 100)
    user_id = random.choice(userlist)
    
    user = User.objects.get(user_id=user_id)
    userlist.remove(user_id)
    
    Familymember.objects.create(
        family_name=familiyname,
        family_gender = familygender,
        family_age = familyage,
        family_height = familyheight,
        family_weight = familyweight,
        user = user
    )
    family = Familymember.objects.get(family_name=familiyname,user = user)
    Weight.objects.create(
        weight = familyweight,
        register_time = fake.date_time_this_year(),
        user = user,
        family = family
    )
    
print("データの挿入が完了しました！")
    