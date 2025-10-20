from django.contrib import admin

# Register your models here.
from .models import MetodoPago, TransaccionCaja, Gasto

@admin.register(TransaccionCaja)
class TransaccionCajaAdmin(admin.ModelAdmin):
    list_display = ('creado_en', 'tipo', 'monto', 'metodo_pago', 'creado_por', 'documento')
    list_filter = ('tipo', 'metodo_pago', 'creado_por')
    search_fields = ('descripcion',)

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'categoria', 'monto', 'pagado_por')
    list_filter = ('categoria', 'pagado_por')
    search_fields = ('descripcion', 'categoria')

admin.site.register(MetodoPago)