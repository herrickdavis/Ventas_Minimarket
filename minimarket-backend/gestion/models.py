from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Importamos los modelos de nuestras otras apps
from catalogo.models import Producto, VarianteProducto, Unidad, ListaPrecios
from inventario.models import Ubicacion

# --- FASE 3.3: Compras y Proveedores ---

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    contacto = models.CharField(max_length=255, null=True, blank=True)
    ruc = models.CharField(max_length=11, null=True, blank=True, unique=True)
    condiciones_pago = models.TextField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = 'borrador', _('Borrador')
        ENVIADO = 'enviado', _('Enviado')
        PARCIAL = 'parcialmente_recibido', _('Parcialmente Recibido')
        RECIBIDO = 'recibido', _('Recibido')
        CANCELADO = 'cancelado', _('Cancelado')
    
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, verbose_name="Proveedor")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.BORRADOR, verbose_name="Estado")
    fecha_entrega_esperada = models.DateField(null=True, blank=True, verbose_name="Fecha de Entrega Esperada")
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Costo Total")
    numero_documento = models.CharField(max_length=100, null=True, blank=True, verbose_name="N° Documento Proveedor")
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordenes_creadas', verbose_name="Creado por")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"

    def __str__(self):
        return f"OC-{self.id} a {self.proveedor.nombre} ({self.estado})"

class OrdenCompraItem(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='items', verbose_name="Orden de Compra")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    variante = models.ForeignKey(VarianteProducto, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Variante")
    cantidad = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Cantidad")
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT, verbose_name="Unidad")
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Costo Unitario")
    
    numero_lote = models.CharField(max_length=100, null=True, blank=True, verbose_name="N° Lote")
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Vencimiento")

    class Meta:
        verbose_name = "Ítem de Orden de Compra"
        verbose_name_plural = "Ítems de Órdenes de Compra"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

# --- FASE 3.4: Clientes y Ventas ---

class Cliente(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")
    documento_identidad = models.CharField(max_length=20, null=True, blank=True, unique=True, verbose_name="Documento (RUC/DNI)")
    lista_precios = models.ForeignKey(ListaPrecios, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lista de Precios")
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cliente_perfil', verbose_name="Usuario (si aplica)")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre

class SesionPOS(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario (Cajero)")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT, verbose_name="Ubicación (Caja)")
    saldo_apertura = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo Apertura")
    saldo_cierre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Saldo Cierre")
    iniciado_en = models.DateTimeField(auto_now_add=True)
    cerrado_en = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=[('abierta', 'Abierta'), ('cerrada', 'Cerrada')], default='abierta', verbose_name="Estado")

    class Meta:
        verbose_name = "Sesión POS"
        verbose_name_plural = "Sesiones POS"

    def __str__(self):
        return f"Caja {self.id} por {self.usuario.username} ({self.estado})"

class Venta(models.Model):
    class Canal(models.TextChoices):
        POS = 'pos', _('POS (Tienda)')
        WEB = 'web', _('Web (E-commerce)')
    
    class EstadoVenta(models.TextChoices):
        BORRADOR = 'borrador', _('Borrador')
        PEDIDO_RECIBIDO = 'pedido_recibido', _('Pedido Recibido (Web)')
        PENDIENTE_PAGO = 'pendiente_pago', _('Pendiente de Pago')
        COMPLETADA = 'completada', _('Completada')
        CANCELADA = 'cancelada', _('Cancelada')

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name="Cliente")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Vendedor")
    sesion_pos = models.ForeignKey(SesionPOS, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sesión POS")
    canal = models.CharField(max_length=10, choices=Canal.choices, default=Canal.POS, verbose_name="Canal")
    estado = models.CharField(max_length=20, choices=EstadoVenta.choices, default=EstadoVenta.BORRADOR, verbose_name="Estado")
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    estado_pago = models.CharField(max_length=20, default='pendiente', verbose_name="Estado de Pago")
    numero_documento = models.CharField(max_length=100, null=True, blank=True, verbose_name="N° Documento (Boleta/Factura)")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre} - Total: {self.total}"

class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items', verbose_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, verbose_name="Producto")
    variante = models.ForeignKey(VarianteProducto, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Variante")
    cantidad = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Cantidad")
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT, verbose_name="Unidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    costo_en_venta = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True, verbose_name="Costo (COGS)")
    numero_lote_usado = models.CharField(max_length=100, null=True, blank=True, verbose_name="N° Lote Usado")
    
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ítem de Venta"
        verbose_name_plural = "Ítems de Venta"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Venta {self.venta.id}"

# --- FASE 5: E-commerce (Carrito) ---

class Carrito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito {self.id}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variante = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    precio_aplicado = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ítem de Carrito"
        verbose_name_plural = "Ítems de Carrito"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Carrito {self.carrito.id}"