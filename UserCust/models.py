from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    POS = (('manager', 'Менеджер'), ('worker', 'Работник'))
    rules = models.CharField('Тип сотрудника', max_length=255, choices=POS, default='worker')
    position = models.CharField('Должность', max_length=255, null=True, blank=True)
