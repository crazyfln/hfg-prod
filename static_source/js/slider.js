$(document).ready(function(){
    min_val = $('#id_min_value').attr('value');
    max_val = $('#id_max_value').attr('value');
    $('#min-slide-value').html('$'+min_val);
    $('#max-slide-value').html('$'+max_val);
    start_val = [min_val, max_val];
    first_regex = /^(\d{1,})\s/;
    second_regex = /(\d{1,})$/;

    $("#slider").slider('setValue', start_val)
        .on('slide', function(e){
            range = $(".tooltip-inner").html()
            first = first_regex.exec(range)[0];
            second = second_regex.exec(range)[0];
            $('#min-slide-value').html('$'+first)
            $('#max-slide-value').html('$'+second)
        })
        .on('slideStop', function(ev){
            $('#id_min_value').attr('value', first);
            $('#id_max_value').attr('value', second);
            $('#SearchForm').submit()
        });
});
