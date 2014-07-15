$(document).ready(function(){

 $('.count').click(function() {
    $('#facility-map').hide()
    $('#facility-carousel').show()
  })


  $('.map').click(function() {
    $('#facility-carousel').hide()
    $('#facility-map').removeClass('hide')
    $('#facility-map').show()

  })


//not working yet
   $('#profile-list a').click(function (e) {
      e.preventDefault()
      $(this).tab('show')
    })


  $('.listing-preview').click(function() {
    url = $(this).attr("url");
    window.location.href=url;
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

  $('[id^=carousel-selector-]').click(function () {
    var id_selector = $(this).attr("id");
    var id = id_selector.substr(id_selector.length - 1);
    id = parseInt(id);
    $('#facility-carousel').carousel(id);
    $('[id^=carousel-selector-]').removeClass('selected');
    $(this).addClass('selected');
  }); 

    $('#facility-carousel').on('slid.bs.carousel', function (e) {
     var id = $('.item.active').data('slide-number');
     id = parseInt(id);
     $('#carousel-current-image-number').html(id);
     $('[id^=carousel-selector-]').removeClass('selected');
     $('[id^=carousel-selector-' + id + ']').addClass('selected');
   });



    $('#edit_manager_note_form').submit(function() {
      $.ajax({
        data: $(this).serialize(),
        type: $(this).attr('method'),
        url: $(this).attr('action'),
        success: function(response) {
          close()
          },
        error: function() {
          alert('Something went wrong, your message was not saved')
        }
      });
      return false;
    });

    $('.heart-holder').on('click', function(e) {
       
        if ($(this).data('logged_in') == 'yes'){

            // $(this).css('background', 'url(img/icon_hearted.png)')

            hearted = $(this).children('img.heart-hearted');
            notHearted = $(this).children('img.heart-not-hearted');
            hearted.toggle();
            notHearted.toggle();

            $.ajax({
                url:$(this).data('url'),
                error: function(){
                    alert('There was an error, the facility was not favorited');
                    hearted.toggle();
                    notHearted.toggle();
                },
            });
        }
        else if ($(this).data('logged_in') == 'no'){
            $('#Registration-Modal').modal('show')
        }
        return false;
    });


    $('#id_planned_move_date').datepicker();

  });
