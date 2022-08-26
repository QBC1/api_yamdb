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


# Categories, genres, titles
class Category(models.Model):
    """Category model"""

    name = models.CharField(
        max_length=256,
        verbose_name="Category name",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Category slug",
    )

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Genre model"""

    name = models.CharField(
        max_length=256,
        verbose_name="Genre name",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Genre slug",
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Title model"""

    name = models.CharField(
        max_length=100,
        verbose_name="Product name",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="The year of publishing",
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Product category",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titles",
        verbose_name="Product genre",
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Product Description",
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""
    text = models.TextField(max_length=1000, blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewer')
    score = models.IntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
