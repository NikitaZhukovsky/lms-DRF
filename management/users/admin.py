from django.contrib import admin
from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active']


admin.site.register(CustomUser, CustomUserAdmin)
