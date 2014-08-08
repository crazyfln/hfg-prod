$(document).ready(function(){

  
 $('.count').click(function() {
    $('#facility-carousel').show()
    $('#facility-map').html('')
  })


  $('.map').click(function() {
    $('#facility-carousel').hide()
    $('#facility-map').html(mapHtml)
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

  $('.right.carousel-control.main-control').click(function() {
    $('#facility-carousel.carousel').carousel('next');
  });

  $('.left.carousel-control.main-control').click(function() {
    $('#facility-carousel.carousel').carousel('prev');
  });

  $('.right.carousel-control.thumb-control').click(function() {
    $('#thumb-carousel.carousel').carousel('next');
  });

  $('.left.carousel-control.thumb-control').click(function() {
    $('#thumb-carousel.carousel').carousel('prev');
  });
  $('.carousel').carousel({
    pause: "hover"
  });

  $('[id^=carousel-selector-]').click(function () {
    var id_selector = $(this).attr("id");
    var id = id_selector.split('-');
    id = parseInt(id[2]);
    $('#facility-carousel').carousel(id - 1);
    $('[id^=carousel-selector-]').removeClass('selected');
    $(this).addClass('selected');
  }); 

   $('#facility-carousel').on('slid.bs.carousel', function (e) {
     var id = $('.item.active').data('slide-number');
     id = parseInt(id);
     $('#carousel-current-image-number').html(id);
     $('[id^=carousel-selector-]').removeClass('selected');
     $('[id^=carousel-selector-' + id + ']').addClass('selected');
     $('#thumb-carousel').carousel(Math.floor((id-1)/8));
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
        return false;
    });


    $('#id_planned_move_date').datepicker();

  });
