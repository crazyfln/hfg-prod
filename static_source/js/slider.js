$(document).ready(function(){
    min_val = $('#id_min_value').attr('value')
    max_val = $('#id_max_value').attr('value')
    start_val = [min_val, max_val]

    $("#slider").slider('setValue', start_val)
        .on('slideStop', function(ev){
            range = $(".tooltip-inner").html()
            first = /^(\d{1,})\s/;
            second = /(\d{1,})$/;
            first = first.exec(range)[0];
            second = second.exec(range)[0];
            $('#id_min_value').attr('value', first);
            $('#id_max_value').attr('value', second);
            $('#SearchForm').submit()
        });
});
