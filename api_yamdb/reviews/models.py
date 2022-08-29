from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_year

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
        validators=[validate_year],
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
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(verbose_name='Рейтинг')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
