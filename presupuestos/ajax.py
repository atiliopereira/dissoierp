import json

from django.http.response import HttpResponse

from materiales.models import Material
from presupuestos.models import Item


def get_presupuesto_item(request):
    item_id = request.GET['item_id']

    resultset = []

    if not item_id:
        return HttpResponse(json.dumps(resultset), content_type='application/json')
    item = Item.objects.filter(id=item_id)

    if item:
        item = Item.objects.get(id=item_id)
        resultset.append({
            "precio_unitario": str(item.get_precio_unitario_venta()).replace('.', ','),
            "cantidad_unidades": str(item.cantidad_unidades).replace('.', ','),
            "subtotal": str(item.precio_venta).replace('.', ','),
            "descripcion": item.descripcion,
        })

    return HttpResponse(json.dumps(resultset), content_type='application/json')


def get_item_material(request):
    material_id = request.GET['material_id']

    resultset = []

    if not material_id:
        return HttpResponse(json.dumps(resultset), content_type='application/json')
    material = Material.objects.filter(id=material_id)

    if material:
        material = Material.objects.get(id=material_id)
        resultset.append({
            "costo": str(material.costo).replace('.', ','),
        })

    return HttpResponse(json.dumps(resultset), content_type='application/json')
