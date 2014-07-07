$(document).ready(function(){

    $('[id^=carousel-selector-]').click(function () {
        var id_selector = $(this).attr("id");
        var id = id_selector.substr(id_selector.length - 1);
        id = parseInt(id);
        $('#facility-carousel').carousel(id);
        $('[id^=carousel-selector-]').removeClass('selected');
        $(this).addClass('selected');
    }); 


    $('.right').click(function() {
        $('.carousel').carousel('next');
    });

    $('.left').click(function() {
        $('.carousel').carousel('prev');
    });

    $('.carousel').carousel({
        pause: "hover"
    });


        // when the carousel slides, auto update
    $('#facility-carousel').on('slid', function (e) {
        var id = $('.item.active').data('slide-number');
        id = parseInt(id);
        $('[id^=carousel-selector-]').removeClass('selected');
        $('[id^=carousel-selector-' + id + ']').addClass('selected');
    });

    $('.heart-holder').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        if ($(this).data('logged_in') == 'yes'){

            // $(this).css('background', 'url(img/icon_hearted.png)')
            heartImg = $(this).children('img')
            heartImg.toggle()

            $.ajax({
                url:$(this).data('url'),
                error: function(){
                    alert('There was an error, the facility was not favorited')
                    heartImg.toggle()
                },
            });
        }
        else if ($(this).data('logged_in') == 'no'){
            $('#Login-Modal').modal('show')
        }
    });
});
