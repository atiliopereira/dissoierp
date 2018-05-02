from django.db import models


class Cliente(models.Model):
    razon_social = models.CharField(max_length=100, verbose_name="nombre o razón social")
    ruc = models.CharField(max_length=15, null=True, blank=True, verbose_name="RUC")
    direccion = models.CharField(max_length=200, null=True, blank=True, verbose_name="dirección")
    telefono = models.CharField(max_length=20, null=True, blank=True, verbose_name="teléfono")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")
    vendedor = models.ForeignKey('funcionarios.Funcionario', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.razon_social


class Marca(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="teléfono")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="e-mail")

    def __str__(self):
        return self.nombre
