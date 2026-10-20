from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        CURATOR = 'curator', 'Куратор'
        STUDENT = 'student', 'Студент'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )
    
    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_curator(self):
        return self.role == self.Roles.CURATOR or self.is_superuser

    def is_student(self):
        return self.role == self.Roles.STUDENT