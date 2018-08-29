from django.contrib import admin
from django.contrib.admin.decorators import register

from items.models import UnidadDeMedida, CategoriaDeItem, Item, DetalleDeItem


@register(UnidadDeMedida)
class UnidadDeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo')
    list_display_links = list_display
    ordering = ('nombre',)
    search_fields = ('nombre', 'simbolo')


@register(CategoriaDeItem)
class CategoriaDeItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria_padre',)
    list_display_links = ('id', 'nombre')
    ordering = ('nombre_completo',)
    search_fields = ('id', 'nombre_completo')


class CategoriaListFilter(admin.SimpleListFilter):

    title = 'Categoria'
    parameter_name = 'categoria_principal'

    def lookups(self, request, model_admin):
        queryset = CategoriaDeItem.objects.all().distinct('categoria_principal__nombre_completo')
        return queryset.values_list('categoria_principal', 'categoria_principal__nombre_completo').order_by(
            'categoria_principal__nombre_completo')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categoria__categoria_principal=self.value())


class DetalleDeItemInline(admin.TabularInline):
    model = DetalleDeItem
    fk_name = 'item_referencia'
    autocomplete_fields = ['item']
    extra = 1


@register(Item)
class ItemAdmin(admin.ModelAdmin):
    change_form_template = 'item_form.html'
    list_display = ('codigo', 'descripcion', 'unidad_de_medida', 'tipo', 'categoria', 'stock_actual', 'precio')
    list_display_links = ('codigo', 'descripcion')
    ordering = ('id', 'descripcion')
    search_fields = ('descripcion', 'codigo')
    list_filter = ('tipo', CategoriaListFilter)
    inlines = []
    autocomplete_fields = ('categoria', )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = (DetalleDeItemInline,)
        return super(ItemAdmin, self).change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = (DetalleDeItemInline,)
        return super(ItemAdmin, self).add_view(request, form_url, extra_context)
