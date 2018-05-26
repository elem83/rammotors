$(function() {
  var projects = $('.project-item').length;
  for (var i = 1; i < (projects+1); i++) {
    Circles.create({
      id: 'circle-'+i,
      radius: 35,
      value: $('#circle-'+i).data('circle-value'),
      maxValue: 100,
      width: 4,
      text: function(value) {
        return value + '%';
      },
      colors: ['#dedede', '#f5f219'],
      duration: 400,
      wrpClass: 'circles-wrp',
      textClass: 'circles-text',
      valueStrokeClass: 'circles-valueStroke',
      maxValueStrokeClass: 'circles-maxValueStroke',
      styleWrapper: true,
      styleText: true
    });
  }
});