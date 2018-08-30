/**
 * Created by ealfonzo on 09/01/17.
 */

$(document).ready(function () {

    $('.modal').modal('init');

    $('.boton-modal').click(function(){
        var id = $(this).attr('id');
        var url = $(this)[0].getAttribute('data-url');
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
                    if (data.indexOf('errorlist') !=-1){
                        var html = $(data);
                        ['#modal-content', '#modal-footer'].forEach(function(el){
                            $(el).html($(html).find(el).html());
                        });
                        $('#modal1').find('form').submit(function(event){
                            $.post($(this).attr('action'), $(this).serialize(), function(data) {
                                console.log(data);
                                if (data.indexOf('errorlist') !=-1){
                                    var html = $(data);
                                    ['#modal-content', '#modal-footer'].forEach(function(el){
                                        $(el).html($(html).find(el).html());
                                    });
                                }else {
                                    // $('#modal1').modal('close');
                                    window.location.reload();

                                }
                            });
                            return false;
                        });
                    }else {
                        // $('#modal1').modal('close');
                        window.location.reload();

                    }
                });
                return false;
            });

            $('#modal-cargando').hide();
        });

    });

    $('#modal-close').click(function () {
        $('#modal1').modal('close');
    });

    $('#modal1').on('hidden.bs.modal', function(){
        ['#modal-content', '#modal-footer'].forEach(function(el){
            $('el').html('');
        });
        $('#modal-content').html('<p id="modal-cargando">Cargando...</p>');
    });
    $("form").submit(function() {
        $(this).submit(function() {
            return false;
        });
        return true;
    });
});