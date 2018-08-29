from django.db import models

from items.constants import TipoItem


class UnidadDeMedida(models.Model):
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"

    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, verbose_name="Símbolo")

    def __str__(self):
        return self.nombre


class CategoriaDeItem(models.Model):
    class Meta:
        verbose_name = "categoría de items"
        verbose_name_plural = "categorías de items"

    nombre = models.CharField(max_length=100, unique=True)
    nombre_completo = models.CharField(max_length=500, editable=False, null=True)
    categoria_padre = models.ForeignKey("self", related_name='categoria_fk', null=True, blank=True,
                                        on_delete=models.CASCADE)
    categoria_principal = models.ForeignKey("self", related_name='categoria_raiz', null=True, blank=True,
                                            on_delete=models.CASCADE, editable=False)

    def save(self, *args, **kwargs):
        if self.categoria_padre is not None:
            self.nombre_completo = self.categoria_padre.nombre_completo + " " + self.nombre
            categoria_raiz = self.categoria_padre
            while categoria_raiz.categoria_padre is not None:
                categoria_raiz = categoria_raiz.categoria_padre
            self.categoria_principal = categoria_raiz
        else:
            self.nombre_completo = self.nombre
            if self.pk:
                self.categoria_principal = self
            else:
                super(CategoriaDeItem, self).save(*args, **kwargs)
                self.categoria_principal = self
        super(CategoriaDeItem, self).save(*args, **kwargs)

        categorias_hijas = CategoriaDeItem.objects.filter(categoria_padre=self)
        for categoria_hija in categorias_hijas:
            categoria_hija.save()

    def __str__(self):
        return self.nombre_completo


class Item(models.Model):
    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"

    tipo = models.CharField(max_length=3, choices=TipoItem.TIPOS, default=TipoItem.PRODUCTO)
    categoria = models.ForeignKey(CategoriaDeItem, verbose_name="categoría", on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, verbose_name="código", null=True, blank=True)
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="costo de compra")
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="precio de venta")
    stock_actual = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    stock_minimo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    es_insumo = models.BooleanField(default=False, help_text="Los insumos no requieren OT para retiro")
    coeficiente_de_cantidad = models.DecimalField(decimal_places=2, max_digits=6, default=1,
                            help_text="Use esta opción cuando su cálculo de items corresponde a varias unidades")
    es_plantilla = models.BooleanField(verbose_name="Guardar como plantilla?", default=False)

    def __str__(self):
        return self.categoria.nombre_completo + " " + self.descripcion

    def get_categoria_padre(self):
        categoria = self.categoria
        while categoria.categoria_padre is not None:
            categoria = categoria.categoria_padre

        return categoria


class DetalleDeItem(models.Model):
    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'
    item_referencia = models.ForeignKey(Item, related_name='item_fk', on_delete=models.CASCADE,
                                            editable=False, null=True)
    item = models.ForeignKey(Item, related_name='item_detalle', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2, default=1)
