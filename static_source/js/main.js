$(document).ready(function(){
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
    // when the carousel slides, auto update
 $('#facility-carousel').on('slid', function (e) {
     var id = $('.item.active').data('slide-number');
     id = parseInt(id);
     $('[id^=carousel-selector-]').removeClass('selected');
     $('[id^=carousel-selector-' + id + ']').addClass('selected');
 });
});
