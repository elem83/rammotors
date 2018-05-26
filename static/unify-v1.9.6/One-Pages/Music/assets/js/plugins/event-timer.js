$(function() {
  var till = '2017/06/02';
  $('.event-timer').countdown(till, function(event) {
    jQuery(".event-timer__month").html(event.strftime('' + '%m'));
    jQuery(".event-timer__days").html(event.strftime('' + '%d'));
    jQuery(".event-timer__hours").html(event.strftime('' + '%H'));
    jQuery(".event-timer__minutes").html(event.strftime('' + '%M'));
    jQuery(".event-timer__seconds").html(event.strftime('' + '%S'));
  });
});