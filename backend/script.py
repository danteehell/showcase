import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()
from showcase.models import *
from tasks.models import *



#Это скрипт для заполнения бд более-менее адекватными данными.
#Он один на всё приложение, просто меняем модель/поля.