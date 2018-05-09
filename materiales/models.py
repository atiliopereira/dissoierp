from django.apps import apps
from django.db import models


class UnidadDeMedida(models.Model):
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"

    nombre = models.CharField(max_length=100)
    simbolo = models.CharField(max_length=10, verbose_name="Símbolo")

    def __str__(self):
        return self.nombre


class CategoriaDeMateriales(models.Model):
    class Meta:
        verbose_name = "categoría de materiales"
        verbose_name_plural = "categorías de materiales"

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
                super(CategoriaDeMateriales, self).save(*args, **kwargs)
                self.categoria_principal = self
        super(CategoriaDeMateriales, self).save(*args, **kwargs)

        categorias_hijas = CategoriaDeMateriales.objects.filter(categoria_padre=self)
        for categoria_hija in categorias_hijas:
            categoria_hija.save()

    def __str__(self):
        return self.nombre_completo


class Material(models.Model):
    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materiales"

    codigo = models.CharField(max_length=20, verbose_name="código", null=True, blank=True)
    descripcion = models.CharField(max_length=150, verbose_name="descripción")
    unidad_de_medida = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaDeMateriales, verbose_name="categoría", on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="costo de compra")
    precio = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="precio de venta")
    stock_actual = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=False)
    stock_minimo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    es_insumo = models.BooleanField(default=False, help_text="Los insumos no requieren OT para retiro")

    def __str__(self):
        return self.categoria.nombre_completo + " " + self.descripcion

    def get_categoria_padre(self):
        categoria = self.categoria
        while categoria.categoria_padre is not None:
            categoria = categoria.categoria_padre

        return categoria