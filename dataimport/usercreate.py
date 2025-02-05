
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

genders = ['0', '1']
# 重複しないメールアドレスを生成するためのセット
email_set = set()
is_superuser = '0'
is_staff = '0'
family = '0'
deleteflag ='0'
subscribeflag = '0'
is_active = '1'

for i in range(100):
    email = fake.email()
    while email in email_set:
        email = fake.email()
    email_set.add(email)
    name = fake.name()
    gender = random.choice(genders)
    age = fake.date_of_birth(minimum_age=18, maximum_age=75)
    formatted_age = age.strftime("%Y/%m/%d")
    height = random.uniform(150, 190)
    weight = random.uniform(50, 100)
    password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    last_login = fake.date_time_this_year()
    date_joined = fake.date_time_this_year()
    
    user =User.objects.create(
            name=name, 
            password=password,
            email =email,
            gender=gender,
            age=formatted_age,
            height=height,
            weight=weight,
            is_superuser=is_superuser,
            is_staff=is_staff,
            family=family,
            last_login=last_login,
            deleteflag=deleteflag,
            subscribeflag=subscribeflag,
            subjoin="",
            unsub="",
            is_active=is_active,
            date_joined=date_joined,
    )
    Familymember.objects.create(
        family_name = name,
        family_gender = gender,
        family_age = formatted_age,
        family_height = height,
        family_weight = weight,
        user = User.objects.get(email=email)
    )
    Weight.objects.create(
        weight = weight,
        register_time = date_joined,
        user = User.objects.get(email=email),
        family = Familymember.objects.get(family_name=name, user=User.objects.get(email=email))
    )
    