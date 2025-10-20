from django.contrib import admin
from .models import (
    Categoria, Marca, ClaseImpuesto, Unidad, 
    ConversionUnidad, Producto, VarianteProducto, ComboProducto,
    ListaPrecios, ReglaListaPrecios
)

class ReglaListaPreciosInline(admin.TabularInline):
    model = ReglaListaPrecios
    extra = 1

@admin.register(ListaPrecios)
class ListaPreciosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    inlines = [ReglaListaPreciosInline]

class VarianteProductoInline(admin.TabularInline):
    model = VarianteProducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sku', 'tipo', 'categoria', 'marca', 'unidad_base', 'es_vendible')
    list_filter = ('tipo', 'categoria', 'marca', 'es_vendible')
    search_fields = ('nombre', 'sku')
    inlines = [VarianteProductoInline]

# Registros base
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(ClaseImpuesto)
admin.site.register(Unidad)
admin.site.register(ConversionUnidad)
admin.site.register(VarianteProducto)
admin.site.register(ComboProducto)