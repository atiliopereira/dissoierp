$(document).ready(function () {

    $('.modal').modal('init');

    $('select.boton-modal').change(function(){
        var id = $(this).attr('id');
        var url = $(this)[0].getAttribute('data-url');
        url = url + '?estado='+this.options[this.selectedIndex].value+'&estado_display='+this.options[this.selectedIndex].text;
        $(id).attr('data-url', url);
        console.log(url);
        $('#modal-cargando').show();
        $('#modal1').modal('open');
        $.get(url, function(data){
            var html = $(data);
            ['#modal-content', '#modal-footer'].forEach(function(el){
                $(el).html($(html).find(el).html());
            });

            $('#modal1').find('form').submit(function(event){
                $.post($(this).attr('action'), $(this).serialize(), function(data) {
                    console.log(data);
                    if (data.hasOwnProperty('error')){
                        $('#modal-content').html("Error al procesar" +
                            "<p>"+data.error+"</p>");
                        $('#modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button>');
                    } else {
                        $('#modal1').modal('close');
                        window.location.reload(true)
                    }
                });
                return false;
            });

            $('#modal-cargando').hide();
        })
    });

    $('#modal1').on('hidden.bs.modal', function(){
        ['#modal-content', '#modal-footer'].forEach(function(el){
            $('el').html('');
        });
        $('#modal-content').html('<p id="modal-cargando">Cargando...</p>');
    });
});