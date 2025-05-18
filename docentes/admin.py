from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Docente, Administrador

class CustomUserAdmin(UserAdmin):
    model = Docente
    list_display = ('correo', 'nombre', 'apellido', 'rol', 'activo', 'is_staff', 'is_superuser')
    list_filter = ('rol', 'activo', 'is_staff', 'is_superuser')
    search_fields = ('correo', 'nombre', 'apellido', 'cedula')
    ordering = ('correo',)
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'telefono', 'cedula', 'activo', 'rol')}),
        ('Permisos', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'apellido', 'telefono', 'cedula', 'password1', 'password2', 'rol', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(Docente, CustomUserAdmin)
admin.site.register(Administrador, CustomUserAdmin)
