from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Importamos los modelos del catálogo que acabamos de crear
from catalogo.models import Producto, VarianteProducto, Unidad

# Para el Polimorfismo (Punto 2 del Plan)
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# --- Modelos de Inventario (Punto 3.2 del Plan) ---

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True) # Ej: "Almacén Principal", "Piso de Venta", "Mermas"
    es_vendible = models.BooleanField(default=False) # Solo el stock en "Piso de Venta" es vendible
    
    class TipoUbicacion(models.TextChoices):
        TIENDA = 'tienda', _('Tienda')
        ALMACEN = 'almacen', _('Almacén')
        DEVOLUCION = 'devolucion', _('Devoluciones')
        VIRTUAL = 'virtual', _('Virtual') # Para ajustes

    tipo = models.CharField(max_length=20, choices=TipoUbicacion.choices, default=TipoUbicacion.ALMACEN)
    
    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"

    def __str__(self):
        return self.nombre

class MovimientoStock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    variante = models.ForeignKey(VarianteProducto, on_delete=models.PROTECT, null=True, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    
    cantidad = models.DecimalField(max_digits=12, decimal_places=4) 
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)

    class TipoMovimiento(models.TextChoices):
        COMPRA = 'compra', _('Compra')
        VENTA = 'venta', _('Venta')
        TRASLADO_ENTRADA = 'traslado_entrada', _('Traslado (Entrada)')
        TRASLADO_SALIDA = 'traslado_salida', _('Traslado (Salida)')
        AJUSTE = 'ajuste', _('Ajuste')
        DEVOLUCION_ENTRADA = 'devolucion_entrada', _('Devolución (Entrada)')
        DEVOLUCION_SALIDA = 'devolucion_salida', _('Devolución (Salida)')

    tipo_movimiento = models.CharField(max_length=20, choices=TipoMovimiento.choices)
    
    numero_lote = models.CharField(max_length=100, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    documento = GenericForeignKey('content_type', 'object_id')
    
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock (Ledger)"
        ordering = ['-creado_en'] 

    def __str__(self):
        signo = "+" if self.cantidad > 0 else ""
        return f"[{self.creado_en.strftime('%Y-%m-%d')}] {self.tipo_movimiento}: {signo}{self.cantidad} {self.unidad.codigo}"

class AjusteStock(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    motivo = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ajuste de Stock"
        verbose_name_plural = "Ajustes de Stock"

    def __str__(self):
        return f"Ajuste {self.id} - {self.motivo}"
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    motivo = models.CharField(max_length=255) # Ej: "Merma por vencimiento", "Robo", "Stock Inicial"
    creado_en = models.DateTimeField(auto_now_add=True)
    
    # Este modelo "AjusteStock" será el "documento" polimórfico
    # para los MovimientoStock de tipo AJUSTE.
    
    class Meta:
        verbose_name = "Ajuste de Stock"
        verbose_name_plural = "Ajustes de Stock"

    def __str__(self):
        return f"Ajuste {self.id} - {self.motivo}"