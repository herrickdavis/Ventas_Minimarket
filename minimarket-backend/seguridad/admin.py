from django.contrib import admin
from .models import RegistroActividad

@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('creado_en', 'usuario', 'accion', 'objeto')
    list_filter = ('usuario', 'content_type', 'accion')
    search_fields = ('usuario__username', 'accion')
    readonly_fields = ('creado_en', 'usuario', 'accion', 'content_type', 'object_id', 'objeto', 'datos_anteriores', 'datos_nuevos', 'ip', 'user_agent')
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False