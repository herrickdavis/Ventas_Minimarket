from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class RegistroActividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuario")
    accion = models.CharField(max_length=255, verbose_name="Acción")
    
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Objeto")
    object_id = models.PositiveIntegerField(null=True, verbose_name="ID Objeto")
    objeto = GenericForeignKey('content_type', 'object_id')
    
    datos_anteriores = models.JSONField(null=True, blank=True, verbose_name="Datos Anteriores")
    datos_nuevos = models.JSONField(null=True, blank=True, verbose_name="Datos Nuevos")
    
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP")
    user_agent = models.CharField(max_length=255, null=True, blank=True, verbose_name="User Agent")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Actividad"
        verbose_name_plural = "Registros de Actividad (Auditoría)"
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        username = self.usuario.username if self.usuario else "Sistema"
        return f"{username} - {self.accion} - {self.creado_en.strftime('%Y-%m-%d %H:%M')}"