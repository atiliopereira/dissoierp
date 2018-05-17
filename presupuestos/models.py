from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

from presupuestos.constants import EstadoPresupuesto


class Item(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=3000, null=True, blank=True)
    coeficiente_cantidad = models.DecimalField("Coeficiente de Cantidad", decimal_places=2, max_digits=6, default=1,
                                               help_text="Use esta opción cuando su cálculo de materiales corresponde a varias unidades")
    cantidad_unidades = models.DecimalField("Cantidad de Unidades", decimal_places=2, max_digits=6, default=1)
    precio_venta = models.DecimalField("Precio de Venta", decimal_places=2, max_digits=12, default=0.0)
    costo_item = models.DecimalField("Costo del Item", decimal_places=2, max_digits=12, default=0.0)
    porcentaje_iva = models.DecimalField("Porcentaje de IVA", decimal_places=2, max_digits=5, default=10)
    es_plantilla = models.BooleanField(verbose_name="Guardar como plantilla?", default=False,)

    def __str__(self):
        return self.nombre

    def get_precio_unitario_venta(self):
        if self.cantidad_unidades == 0:
            return 0
        else:
            return round(self.precio_venta / self.cantidad_unidades)

    def get_costo_unitario(self):
        if self.coeficiente_cantidad == 0:
            return 0
        else:
            return round(self.costo_item / self.coeficiente_cantidad)

    def get_costo_total(self):
        costo_unitario = self.get_costo_unitario()
        return round(costo_unitario * self.cantidad_unidades)


class DetalleDeItem(models.Model):
    class Meta:
        verbose_name_plural = 'Costeo'
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    material = models.ForeignKey('materiales.Material', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    def get_costo(self):
        return self.material.costo

    def get_subtotal(self):
        return self.cantidad * self.material.costo


class Presupuesto(models.Model):
    version = models.IntegerField(default=1, editable=False)
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(default=datetime.now, null=True, blank=True)
    fecha_solicitada = models.DateField(null=True, blank=True)
    nombre_del_trabajo = models.CharField(max_length=200)
    comentarios = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=3, choices=EstadoPresupuesto.ESTADOS, default=EstadoPresupuesto.PENDIENTE)
    anulado = models.BooleanField(default=False, editable=False)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    responsable = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "-" + self.nombre_del_trabajo


class DetalleDePresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
