from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Docente, Administrador

class CustomUserAdmin(UserAdmin):
    model = Docente
    list_display = ('cedula', 'nombre', 'apellido', 'rol', 'activo', 'is_staff', 'is_superuser')
    list_filter = ('rol', 'activo', 'is_staff', 'is_superuser')
    search_fields = ('cedula', 'nombre', 'apellido')
    ordering = ('cedula',)
    fieldsets = (
        (None, {'fields': ('cedula', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'activo', 'rol')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cedula', 'nombre', 'apellido', 'password1', 'password2', 'rol', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Docente, CustomUserAdmin)
admin.site.register(Administrador, CustomUserAdmin)
