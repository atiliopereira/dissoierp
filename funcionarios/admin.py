from django.contrib import admin
from django.contrib.admin.decorators import register

from funcionarios.models import Funcionario


@register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'usuario')
    ordering = ('nombres', 'apellidos',)
    search_fields = ('nombres', 'apellidos', 'usuario')
