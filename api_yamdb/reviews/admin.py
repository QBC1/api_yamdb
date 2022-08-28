from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review')
    list_display_links = ('pk', 'text', 'author')
    list_editable = ('text', 'author')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_display_links = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'title', 'score', 'pub_date')
    list_display_links = ('pk', 'text', 'author', 'score')
    list_editable = ('text', 'author', 'score')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'genre', 'description')
    list_display_links = ('pk', 'name', 'year', 'category', 'genre')
    list_editable = ('name', 'year', 'category', 'genre', 'description')


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name',
                    'last_name', 'email', 'bio', 'role')
    list_display_links = ('pk', 'username', 'first_name', 'last_name',)
    list_editable = ('role',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
