from daterange_filter.filter import DateRangeFilter
from django.contrib import admin
from django.contrib.admin import register

from presupuestos.models import DetalleDePresupuesto, AdjuntoDePresupuesto, Presupuesto


class DetalleDePresupuestoInline(admin.TabularInline):
    model = DetalleDePresupuesto
    extra = 1


class AdjuntoDePresupuestoInline(admin.StackedInline):
    model = AdjuntoDePresupuesto
    extra = 0


@register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    inlines = (DetalleDePresupuestoInline, AdjuntoDePresupuestoInline)
    list_display = ('fecha_de_creacion', 'descripcion', 'cliente', 'estado')
    search_fields = ('descripcion', 'cliente')
    list_filter = ['estado', ('fecha_de_creacion', DateRangeFilter), ]
