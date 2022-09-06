from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from api_yamdb.settings import ADMIN, MODERATOR, ROLE_CHOICES, USER


class User(AbstractUser):
    """Модель пользователя, добавлено поле bio и role,
    так же поле email теперь должно быть уникальным и не может быть пустым """

    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(
        choices=ROLE_CHOICES,
        blank=True, max_length=50,
        default=USER)
    username = models.CharField(
        max_length=60,
        unique=True,
        validators=[UnicodeUsernameValidator(), ],
        verbose_name='username',
        blank=False)
    email = models.EmailField(
        unique=True, blank=False, max_length=254, verbose_name='email address')
    confirmation_code = models.CharField(max_length=50, blank=True)
    data_confirmation_code = models.DateTimeField(
        auto_now_add=True,)

    class Meta:
        ordering = ['role']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR
