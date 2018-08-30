from datetime import date

from django.contrib.auth.models import User
from django.db import models

from presupuestos.constants import EstadoPresupuesto


class Presupuesto(models.Model):
    descripcion = models.CharField(max_length=200)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.PROTECT)
    fecha_de_creacion = models.DateField(default=date.today, editable=False)
    forma_de_pago = models.CharField(max_length=200, null=True, blank=True)
    validez = models.CharField(max_length=100, default="8 dias", null=True, blank=True)
    observaciones = models.TextField(max_length=300, null=True, blank=True)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    estado = models.CharField(max_length=3, choices=EstadoPresupuesto.ESTADOS, default=EstadoPresupuesto.BORRADOR)
    creador = models.ForeignKey(User, related_name='creado_por', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + "-" + self.descripcion


class DetalleDePresupuesto(models.Model):
    presupuesto = models.ForeignKey('presupuestos.Presupuesto', on_delete=models.CASCADE)
    item = models.ForeignKey('items.Item', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
