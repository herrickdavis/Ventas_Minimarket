from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100, unique=True) # Efectivo, Tarjeta, Yape, Plin
    comision = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"

    def __str__(self):
        return self.nombre

class TransaccionCaja(models.Model):
    class TipoTransaccion(models.TextChoices):
        VENTA = 'venta', _('Venta')
        COMPRA = 'compra', _('Compra')
        GASTO = 'gasto', _('Gasto')
        APERTURA_CAJA = 'apertura_caja', _('Apertura de Caja')
        CIERRE_CAJA = 'cierre_caja', _('Cierre de Caja')
        AJUSTE = 'ajuste', _('Ajuste')

    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto (+/-)")
    tipo = models.CharField(max_length=20, choices=TipoTransaccion.choices, verbose_name="Tipo")
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT, verbose_name="Método de Pago")
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    documento = GenericForeignKey('content_type', 'object_id')
    
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Creado por")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transacción de Caja"
        verbose_name_plural = "Transacciones de Caja (Ledger)"
        ordering = ['-creado_en']

    def __str__(self):
        return f"[{self.tipo}] {self.monto} via {self.metodo_pago.nombre}"

class Gasto(models.Model):
    categoria = models.CharField(max_length=100, verbose_name="Categoría") # Ej: "Alquiler", "Luz", "Sueldos"
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto")
    fecha = models.DateField(verbose_name="Fecha")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")
    pagado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Pagado por")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"

    def __str__(self):
        return f"Gasto: {self.categoria} - {self.monto}"