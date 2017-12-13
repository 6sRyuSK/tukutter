$(function(){
  $(window).scroll(function() {
    $('ul').toggleClass('fixed', $(this).scrollTop() > 105);
    $('.stream').toggleClass('fixed', $(this).scrollTop() > 105);
  });
  $('.list-search').click(function(){
    $('.tweet').hide();
    $('.search').show();
  });
  $('.list-tweet').click(function(){
    $('.search').hide();
    $('.tweet').show();
  });
});