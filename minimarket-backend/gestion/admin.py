from django.contrib import admin

# Register your models here.
from .models import (
    Proveedor, OrdenCompra, OrdenCompraItem, Cliente, 
    SesionPOS, Venta, VentaItem, Carrito, CarritoItem
)

class OrdenCompraItemInline(admin.TabularInline):
    model = OrdenCompraItem
    extra = 1

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'estado', 'costo_total', 'creado_en')
    list_filter = ('estado', 'proveedor')
    search_fields = ('id', 'proveedor__nombre')
    inlines = [OrdenCompraItemInline]

class VentaItemInline(admin.TabularInline):
    model = VentaItem
    extra = 0
    readonly_fields = ('producto', 'variante', 'cantidad', 'unidad', 'precio_unitario', 'subtotal')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'canal', 'estado', 'total', 'creado_en')
    list_filter = ('canal', 'estado', 'cliente')
    search_fields = ('id', 'cliente__nombre')
    inlines = [VentaItemInline]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento_identidad', 'telefono', 'email', 'lista_precios')
    search_fields = ('nombre', 'documento_identidad')

admin.site.register(Proveedor)
admin.site.register(SesionPOS)
admin.site.register(Carrito)