from django.db import models
from django.utils.translation import gettext_lazy as _

# --- Modelos Base (Punto 3.1 del Plan) ---

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategorias')

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class ClaseImpuesto(models.Model):
    nombre = models.CharField(max_length=100, unique=True) # Ej: "IGV 18%", "Exonerado"
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Clase de Impuesto"
        verbose_name_plural = "Clases de Impuestos"

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

class Unidad(models.Model):
    codigo = models.CharField(max_length=10, unique=True) # Ej: "kg", "g", "ud", "lt", "ml"
    nombre = models.CharField(max_length=50)
    decimales = models.PositiveSmallIntegerField(default=0) 

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class ConversionUnidad(models.Model):
    unidad_origen = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='conversiones_origen')
    unidad_destino = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='conversiones_destino')
    factor = models.DecimalField(max_digits=14, decimal_places=6)

    class Meta:
        verbose_name = "Conversión de Unidad"
        verbose_name_plural = "Conversiones de Unidades"

    def __str__(self):
        return f"1 {self.unidad_origen.codigo} = {self.factor} {self.unidad_destino.codigo}"

# --- Modelos Principales de Producto (Punto 3.1) ---

class Producto(models.Model):
    
    class TipoProducto(models.TextChoices):
        SIMPLE = 'simple', _('Simple')
        VARIABLE = 'variable', _('Variable')
        COMBO = 'combo', _('Combo')

    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TipoProducto.choices, default=TipoProducto.SIMPLE)

    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    clase_impuesto = models.ForeignKey(ClaseImpuesto, on_delete=models.SET_NULL, null=True, blank=True)
    unidad_base = models.ForeignKey(Unidad, on_delete=models.PROTECT, related_name='productos')

    es_vendible = models.BooleanField(default=True)
    es_comprable = models.BooleanField(default=True)
    es_producto_fisico = models.BooleanField(default=True)
    
    umbral_bajo_stock = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    imagen_url = models.CharField(max_length=500, null=True, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} ({self.sku or ''})"

class VarianteProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='variantes')
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    datos_atributo = models.JSONField(null=True, blank=True)
    precio_sobrescrito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unidad_base = models.ForeignKey(Unidad, on_delete=models.PROTECT, null=True, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Productos"

    def __str__(self):
        return f"{self.producto.nombre} - {self.nombre}"

class ComboProducto(models.Model):
    producto_combo = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='items_combo')
    producto_item = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='en_combos')
    variante_item = models.ForeignKey(VarianteProducto, on_delete=models.PROTECT, null=True, blank=True)
    cantidad_item = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        verbose_name = "Item de Combo"
        verbose_name_plural = "Items de Combos"

    def __str__(self):
        return f"Combo '{self.producto_combo.nombre}' contiene {self.cantidad_item} de '{self.producto_item.nombre}'"

# --- FASE 3.5: Precios (Aquí pertenecen) ---

class ListaPrecios(models.Model):
    nombre = models.CharField(max_length=100, unique=True) # Ej: "Minorista", "Mayorista"
    descripcion = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Lista de Precio"
        verbose_name_plural = "Listas de Precios"

    def __str__(self):
        return self.nombre

class ReglaListaPrecios(models.Model):
    lista_precio = models.ForeignKey(ListaPrecios, on_delete=models.CASCADE, related_name='reglas')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    variante = models.ForeignKey(VarianteProducto, on_delete=models.CASCADE, null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_minima = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Regla de Lista de Precio"
        verbose_name_plural = "Reglas de Listas de Precios"

    def __str__(self):
        return f"Regla para {self.lista_precio.nombre} - Precio: {self.precio}"