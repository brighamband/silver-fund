import csv, sys, os, django

project_dir = "C://Coding/SF/Silver-Fund-Web-App/backend"
sys.path.append(project_dir)
os.environ["DJANGO_SETTINGS_MODULE"] = "backend.settings"
django.setup()

from django.contrib.auth import authenticate
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

file = input("Enter csv file containing new users:\t\t(ex: 'users-fall-2020.csv')\n")

data = csv.reader(open(file), delimiter=",")


print("\nResults:\n")
index = 0

for row in data:
    index = index + 1

    new_user = User()
    new_user.first_name = row[0]
    new_user.last_name = row[1]
    new_user.username = row[2]
    new_user.email = row[3]
    new_user.password = make_password(row[4])
    new_user.is_active = "0"
    new_user.save()

    print("Successfully created user (" + str(index) + ").")

print("\n" + str(index) + " users created.")
