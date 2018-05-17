from django.contrib import admin
from django.contrib.admin.decorators import register
from django.http.response import HttpResponseRedirect

from presupuestos.forms import DetalleDeItemForm, ItemForm, DetalleDePresupuestoForm, PresupuestoForm
from presupuestos.models import DetalleDeItem, Item, Presupuesto, DetalleDePresupuesto


class DetalleDeItemInline(admin.TabularInline):
    model = DetalleDeItem
    form = DetalleDeItemForm
    autocomplete_fields = ['material']
    extra = 0


@register(Item)
class ItemAdmin(admin.ModelAdmin):
    class Media:
        js = ('/static/js/autoNumeric.js', '/static/js/decimales.js', 'item.js')

    save_as = True

    form = ItemForm
    list_display = ('nombre', 'descripcion', 'precio_venta')
    ordering = ('-id',)
    search_fields = ('nombre', 'descripcion')
    fieldsets = (
        ('Datos del Item', {
            'fields': [('nombre',), ('descripcion',), ('es_plantilla',)]
        }),
        ('Calculo de precio', {
            'fields': [('precio_venta',),
                       ('coeficiente_cantidad', 'precio_unitario_venta'),
                       ('cantidad_unidades', 'costo_total'),
                       ('costo_unitario',),
                       ('costo_item',)]
        }),

    )

    inlines = (DetalleDeItemInline,)

    def save_model(self, request, obj, form, change):
        if "_saveasnew" in request.POST:
            obj.pk = None
        return super(ItemAdmin, self).save_model(request, obj, form,
                                                 change)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}
        extra['guardar_como'] = True
        return super(ItemAdmin, self).change_view(request, object_id, form_url, extra_context=extra)

    def has_module_permission(self, request):
        return False


class DetalleDelPresupuestoInline(admin.TabularInline):
    model = DetalleDePresupuesto
    form = DetalleDePresupuestoForm

    fieldsets = (
        (None, {
            'fields': [('item', 'cantidad', 'precio_unitario', 'subtotal')]
        }),)
    extra = 1


@register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/autoNumeric.js', 'js/decimales.js', 'presupuesto.js')

    inlines = (DetalleDelPresupuestoInline,)
    form = PresupuestoForm
    autocomplete_fields = ['cliente']
    list_display = ('nombre_del_trabajo', 'cliente', 'fecha_ingreso',)
    ordering = ('-fecha_ingreso',)
    search_fields = ('nombre_del_trabajo',)

    fieldsets = (
        (None, {
            'fields': [('fecha_ingreso', 'fecha_solicitada'), ('nombre_del_trabajo', 'cliente')]
        }),

        (None, {
            'fields': ['comentarios']
        }),
        (None, {
            'fields': [('descuento', 'total')]
        }),
        (None, {
            'fields': ['responsable']
        }),
    )

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.responsable = request.user
        obj.save()

    def response_add(self, request, obj, post_url_continue=None):
        res = super(PresupuestoAdmin, self).response_add(request, obj, post_url_continue)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def response_change(self, request, obj):
        res = super(PresupuestoAdmin, self).response_change(request, obj)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({'presupuesto_form': PresupuestoForm()})
        return super(PresupuestoAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def response_delete(self, request, obj_display, obj_id):
        res = super(PresupuestoAdmin, self).response_delete(request, obj_display, obj_id)
        if "next" in request.GET:
            return HttpResponseRedirect(request.GET['next'])
        else:
            return res
