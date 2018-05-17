
String.prototype.replace_all =function (busqueda, reemplazo){
    var target = this;
    return target.split(busqueda).join(reemplazo);

};

(function($) {
function calcular_total() {
    var total_general = 0;

    // calculo del costo del item a partir de los subtotales de los materiales
    $('.subtotal_iterable').each(function () {
        var vector = $(this).attr("id").split("-");

        var cantidad = ($('#' + vector[0] + '-' + vector[1] + '-cantidad').val() != '') ? unformat(document.getElementById(vector[0] + '-' + vector[1] + '-cantidad')) : '0';

        var costo = ($('#' + vector[0] + '-' + vector[1] + '-costo').val() != '') ? unformat(document.getElementById(vector[0] + '-' + vector[1] + '-costo')) : '0';

        var subtotal = parseFloat(cantidad) * parseFloat(costo);

        if ((costo != 0) || (cantidad != 0)) {
            $('#' + vector[0] + '-' + vector[1] + '-subtotal').val(parseFloat(subtotal).toString().replace(".", ",")+',00');
            format(document.getElementById(vector[0] + '-' + vector[1] + '-subtotal'));
        } else {
            $('#' + vector[0] + '-' + vector[1] + '-subtotal').val('');
        }

        if ($('#' + vector[0] + '-' + vector[1] + '-subtotal').is(":visible") === true) {
            total_general += subtotal
        }
        var campo_costo = $('#' + vector[0] + '-' + vector[1] + '-' + '-costo');
        campo_costo.val(costo.toString()+',00');
        format(document.getElementById(vector[0] + '-' + vector[1] + '-costo'));
    });


    var costo_item = $('#id_costo_item');
    costo_item.val(parseFloat(total_general).toString().replace(".", ",")+',00');
    format(document.getElementById('id_costo_item'));

    costo_unitario();
    costo_total_y_venta_unitario();
}

function costo_unitario(){
    // selectores ( hago de esta manera para que se pueda usar en otro lado sin tener que editar los selectores cada vez que aparece )

    var s_costo_item = $('#id_costo_item');
    var s_costo_unitario = $('#id_costo_unitario');
    var s_coeficiente_cant = $('#id_coeficiente_cantidad');

    var coef_cant = parseFloat(s_coeficiente_cant.val().toString().replace_all(".", "")) || 0;
    var c_item = parseFloat(s_costo_item.val().toString().replace_all(".", "")) || 0;
    if(coef_cant>0){
        s_costo_unitario.val(parseFloat(Math.round(c_item/coef_cant).toString().replace_all(".", ","))+',00');
    }else{
        s_costo_unitario.val(parseFloat(Math.round(0.0).toString().replace_all(".", ","))+',00');
    }

    format(document.getElementById('id_costo_unitario'));
    format(document.getElementById('id_coeficiente_cantidad'));

}

function costo_total_y_venta_unitario() {
    // selectores ( hago de esta manera para que se pueda usar en otro lado sin tener que editar los selectores cada vez que aparezce )

    var s_cantidad_unidades = $('#id_cantidad_unidades');
    var s_costo_total = $('#id_costo_total');
    var s_precio_unitario_venta = $('#id_precio_unitario_venta');
    var s_precio_venta = $('#id_precio_venta');
    var s_costo_unitario = $('#id_costo_unitario');


    var costo_unitario = parseFloat(s_costo_unitario.val().toString().replace_all(".", "")) || 0;
    var cantidad_unidades = parseFloat(s_cantidad_unidades.val().toString().replace_all(".", "")) || 0;
    var precio_venta = parseFloat(s_precio_venta.val().toString().replace_all(".", "")) || 0;

    s_costo_total.val(parseFloat(Math.round(costo_unitario*cantidad_unidades).toString().replace_all(".", ","))+',00');

    if(cantidad_unidades>0){
        s_precio_unitario_venta.val(parseFloat(Math.round(precio_venta/cantidad_unidades).toString().replace_all(".", ","))+',00');
    }

    format(document.getElementById('id_costo_total'));
    format(document.getElementById('id_precio_unitario_venta'));
}

$(document).ready(function () {

    // recalcular totales al borrar un item de un detalle no guardador (con botoncito 'x' )
    $('.btn-flat').click(function () {

        setTimeout(function () {
            var campo_decimal = $('.auto');
            campo_decimal.autoNumeric('init',{mDec: 0});
            campo_decimal.css("text-align", "right");
            calcular_total();
            campo_decimal.keyup(function () {
                calcular_total();
            });
        }, 500)

    });

    // calcular totales al editar campos numericos
    $('.auto').keyup(function () {
        calcular_total();
    });

    material_handler();

});

$(document).bind('DOMNodeInserted', function(e) {
    material_handler();
});

function material_handler(){
    $('select').change(function() {
        if($(this).val()){
            try{
                var vector=$(this).attr('id').split('-');


                var id = vector[0];
                if(id=="id_detalledeitem_set"){
                    var optionSelected = $(this).find("option:selected");
                    var valueSelected  = optionSelected.val();
                    $.ajax({
                        data : {'material_id' : valueSelected },
                        url : "/admin/presupuestos/get_item_material",
                        type : "get",
                        success : function(data){
                            var campo_costo = $('#id_detalledeitem_set-'+vector[1]+'-costo');
                            campo_costo.val(data[0].costo);
                            campo_costo.trigger('click')
                        }
                    });
                }
            }catch (ex){
                console.log(ex)
            }
        }
    });
}
})(django.jQuery);