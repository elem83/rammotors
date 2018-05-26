// Created by: Farukham: (https://github.com/farukham/Bootstrap-Animated-Progress-Bars)
jQuery(function() {
  jQuery('.progress-block-1').each(function() {
    var el = $(this);
    el.appear(function() {
      el.animate({
        opacity: 1,
        left: '0'
      }, 800);
      var b = el.find('.progress-bar').attr('data-progress-value')*100/el.find('.progress-bar').attr('data-progress-goal');
      el.find('.progress-bar').animate({
        width: b + '%'
      }, 100, 'linear');
      el.find('.progress-bar').html('<span>$ ' + el.find('.progress-bar').attr('data-progress-value-title') + '</span>');
      el.find('.progress__time-left').children('em').html(el.find('.progress-bar').attr('data-progress-time'));
      el.find('.progress__goal').children('em').html('$' + el.find('.progress-bar').attr('data-progress-goal-title'));
    });
  });
  jQuery('.progress-block-2').each(function() {
    var el = $(this);
    el.appear(function() {
      el.animate({
        opacity: 1,
        left: '0'
      }, 800);
      var b = el.find('.progress-bar').attr('data-progress-status');
      el.find('.progress-bar').animate({
        width: b + '%'
      }, 100, 'linear');
      el.find('.progress-bar').html('<span>' + el.find('.progress-bar').attr('data-progress-status') + '%</span>');
      el.find('.progress__time-left').children('em').html(el.find('.progress-bar').attr('data-progress-time'));
      el.find('.progress__goal').children('em').html('$' + el.find('.progress-bar').attr('data-progress-goal-title'));
    });
  });
});