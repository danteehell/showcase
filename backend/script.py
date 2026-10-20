import os
import django
import datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from showcase.models import *
from users.models import User



#Это скрипт для заполнения бд более-менее адекватными данными.
#Он один на всё приложение, просто меняем модель/поля.


