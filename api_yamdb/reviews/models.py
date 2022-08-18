from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class UserForRegistarions(models.Model):
    username = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50, blank=False)
    confirm_code = models.CharField(max_length=50)
    create_date = models.DateTimeField(
        auto_now_add=True,)


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, blank=False, max_length=50)
    email = models.EmailField(
        blank=False, unique=True, max_length=254, verbose_name='email address')
