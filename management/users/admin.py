from django.contrib import admin
from users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'role', 'is_staff', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']


admin.site.register(CustomUser, CustomUserAdmin)
