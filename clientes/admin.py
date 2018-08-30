from django.contrib import admin
from django.contrib.admin.decorators import register
from clientes.models import Cliente, Marca, Contacto


class MarcaInlineAdmin(admin.TabularInline):
    model = Marca
    extra = 1


class ContactoInlineAdmin(admin.TabularInline):
    model = Contacto
    extra = 1


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'ruc', 'email', 'direccion', 'telefono', 'vendedor')
    search_fields = ('razon_social', 'ruc')
    inlines = [MarcaInlineAdmin, ContactoInlineAdmin]
