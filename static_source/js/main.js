$(document).ready(function(){

  $('#Video-Modal').on('hidden.bs.modal', function () {
    var $frame = $('iframe#vimeo-iframe');

    // saves the current iframe source
    var vidsrc = $frame.attr('src');

    // sets the source to nothing, stopping the video
    $frame.attr('src',''); 

    // sets it back to the correct link so that it reloads immediately on the next window open
    $frame.attr('src', vidsrc);
   });

  var bgImageNumber = 3 // how many bg classes in index.scss
  var bgIndex = 2 // which bg to display next
  var oldIndex = 1 // the default home-bg-image- class specified in html

  window.setInterval(function() {
    if (bgIndex > bgImageNumber) {
      bgIndex = 1;
    };
    $('.home-background').animate({ opacity:.5}, function() {
        $(this).removeClass('home-bg-image-' + oldIndex).addClass('home-bg-image-' + bgIndex).animate({ opacity:1})
        oldIndex = bgIndex
        bgIndex++    
    });

  }, 10000)

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
