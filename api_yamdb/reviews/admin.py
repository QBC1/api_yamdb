from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name',
                    'last_name', 'email', 'bio', 'role')
    list_display_links = ('pk', 'username', 'first_name', 'last_name',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
