from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser


@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    model = CustomerUser
    list_display = ('username', 'email', 'birthday', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('birthday', 'bio', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'birthday', 'bio', 'profile_image', 'is_active', 'is_staff')}
        ),
    )
