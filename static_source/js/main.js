submitParentForm = function() {
    form = $(this).closest('form');
    form.submit();
};  

normalRegistration = function() {
    form = $('#registration-form');
    url = form.data('normal-url');
    form.attr('action',url);
}
getPhoneRegistration = function() {
    form = $('#registration-form');
    url = form.data('get-phone-url');
    form.attr('action', url);
}
tourRequestRegistration = function() {
    form = $('#registration-form');
    url = form.data('tour-request-url');
    form.attr('action', url);
}

$(document).ready(function(){

  $('.normal-registration-button').on('click', function() {
        normalRegistration();
        $('#Registration-Modal-1').modal('show');
  });
  $('#id_room_type').change(submitParentForm);
  $('#id_facility_type').change(submitParentForm);
  $('#searchfield-amenities input').change(submitParentForm);


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
  var NextImg = new Image() 
  NextImg.src = '/static/img/home-background-' + bgIndex + '.jpg'

  window.setInterval(function() {
    $('.home-background').animate({ opacity:.5}, function() {
        $(this).removeClass('home-bg-image-' + oldIndex).addClass('home-bg-image-' + bgIndex).animate({ opacity:1, duration:5000})
        oldIndex = bgIndex
        bgIndex++    
        if (bgIndex > bgImageNumber) {
          bgIndex = 1;
        };
        NextImg.src = 'static/img/home-background-' + bgIndex + '.jpg'
    });

  }, 10000)

  $('.count').click(function() {
    $('#facility-carousel').show()
    $('#facility-map').html('')
  });


  $('.map').click(function() {
    $('#facility-carousel').hide()
    $('#facility-map').html(mapHtml)
  })

  $('#search-community-type-label').tooltip({
    'title':'Community Types Blog',
    'placement':'left'
  });

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

    $('.heart-holder').tooltip({'title':'Save to favorites', });
    
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
            $('#Registration-Modal-1').modal('show')
        }
        return false;
    });

    dateField = $('#id_planned_move_date')
    dateField.datepicker({dateFormat: 'mm-dd-y'});
  });
