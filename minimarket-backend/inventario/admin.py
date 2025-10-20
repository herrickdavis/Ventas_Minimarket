from django.contrib import admin
from .models import Ubicacion, MovimientoStock, AjusteStock

@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('creado_en', 'producto_display', 'tipo_movimiento', 'cantidad', 'unidad', 'ubicacion', 'documento')
    list_filter = ('tipo_movimiento', 'ubicacion')
    search_fields = ('producto__nombre', 'variante__nombre')
    list_display_links = None

    def producto_display(self, obj):
        return obj.variante.nombre if obj.variante else obj.producto.nombre
    producto_display.short_description = "Producto"
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Ubicacion)
admin.site.register(AjusteStock)