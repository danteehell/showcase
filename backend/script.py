import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()
from showcase.models import *



projects = Project.objects.all()

for project in projects:
    project.internship = random.choice([True, False])

    project.save()

#Это скрипт для заполнения бд более-менее адекватными данными.
#Он один на всё приложение, просто меняем модель/поля.