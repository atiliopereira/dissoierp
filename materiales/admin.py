from django.contrib import admin
from django.contrib.admin.decorators import register
from materiales.models import UnidadDeMedida, CategoriaDeMateriales, Material


@register(UnidadDeMedida)
class UnidadDeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'simbolo')
    list_display_links = list_display
    ordering = ('nombre',)
    search_fields = ('nombre', 'simbolo')


@register(CategoriaDeMateriales)
class CategoriaDeMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria_padre',)
    list_display_links = ('id', 'nombre')
    ordering = ('nombre_completo',)
    search_fields = ('id', 'nombre_completo')


class CategoriaListFilter(admin.SimpleListFilter):

    title = 'Categoria'
    parameter_name = 'categoria_principal'

    def lookups(self, request, model_admin):
        queryset = CategoriaDeMateriales.objects.all().distinct('categoria_principal__nombre_completo')
        return queryset.values_list('categoria_principal', 'categoria_principal__nombre_completo').order_by(
            'categoria_principal__nombre_completo')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categoria__categoria_principal=self.value())


@register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion', 'unidad_de_medida', 'categoria', 'stock_actual', 'precio')
    list_display_links = ('codigo', 'descripcion')
    ordering = ('id', 'descripcion')
    search_fields = ['descripcion', 'codigo']
    list_filter = (CategoriaListFilter, )