from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
)


class User(AbstractUser):
    """Модель пользователя, добавлено поле bio и role,
    так же поле email теперь должно быть уникальным и не может быть пустым """

    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(
        choices=ROLE_CHOICES, blank=True, max_length=50, default='user')
    email = models.EmailField(
        unique=True, blank=False, max_length=254, verbose_name='email address')
    confirmation_code = models.CharField(max_length=50, blank=True)
    data_confirmation_code = models.DateTimeField(
        auto_now_add=True,)
