$(document).ready(function(){
    $('#num_pessoas, #num_pessoas_evento').keyup(function(event){
        if($(this).val() == '')
            $(this).val(0)
        qtd_pessoas = parseInt($('#num_pessoas').val());
        qtd_pessoas_evento = parseInt($('#num_pessoas_evento').val());
        $('#num_pessoas_total').val(qtd_pessoas+qtd_pessoas_evento);
    });


    $('#permite_carros_mundo').bind('click', function(){
        $mundo_permite_carros = $(this);
        $('input[name=permite_carro]').attr('checked', $mundo_permite_carros.is(':checked'));
    });
});
