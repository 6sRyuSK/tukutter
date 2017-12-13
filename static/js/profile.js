$(function(){
  $(window).scroll(function() {
    $('ul').toggleClass('fixed', $(this).scrollTop() > 105);
    $('.profilecard').toggleClass('fixed', $(this).scrollTop() > 105);
  });
});
