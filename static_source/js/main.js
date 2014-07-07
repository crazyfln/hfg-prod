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
      e.stopPropagation();
      if ($(this).data('logged_in') == 'no'){
        $('#Login-Modal').modal('show')
      }
    });

    $('#edit_manager_note_form').submit(function() {
      console.log('boop')
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



  });
