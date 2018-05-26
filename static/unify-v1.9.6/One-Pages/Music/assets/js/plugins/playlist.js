$(function() {
  jQuery('audio').audioPlayer();

  // Accordion
  var next = jQuery('.playlist-section').find('.accordion-toggle');
  next.click(function() {
    jQuery(this).next().slideToggle('fast');
    jQuery('.accordion-content').not(jQuery(this).next()).slideUp('fast');
  });


  $('audio').bind('play', function (event) {
    pauseAllbut($(this).attr("id"));
  });

  $.each($('audio'),function (i,val) {
    $(this).attr({'id':'audio'+i});
  });

  // Function to pause each audios except the one which was clicked
  function pauseAllbut(playTargetId) {
    $.each($('audio'),function(i,val) {
      ThisEachId = $(this).attr('id');
      if (ThisEachId != playTargetId) {
        $('.audioplayer-playpause').each(function() {
          if ($(this).prev().attr('id') != playTargetId) {
            ButtonState = $(this).find('a').html();
            if (ButtonState == 'Pause') {
              $(this).find('a').click();
            }
          }
        });
      }
    });
  }

  $('.playlist-music-audio__next').click(function() {
    var actualAccordion = $(this).parent().parent().parent('.accordion-content');
    belowAccordion = actualAccordion.parent().next().children('.accordion-toggle').first();

    // Toggle it!
    if (belowAccordion.length>0) {
      actualAccordion.first().slideToggle('fast');
      belowAccordion.click()
      belowAccordion.next().first().children().children().children().children('.audioplayer-playpause').click();
    } else {
      alert('No other song to play!');
    }
  });

  $('.playlist-music-audio__prev').click(function() {
    var actualAccordion = $(this).parent().parent().parent('.accordion-content');
    aboveAccordion = actualAccordion.parent().prev().children('.accordion-toggle').first();

    // Toggle it!
    if (aboveAccordion.length>0) { // If an accordion is found
      actualAccordion.first().slideToggle('fast'); // Toggles actual accordion.
      aboveAccordion.click() //.slideToggle('fast');
      aboveAccordion.next().first().children().children().children().children('.audioplayer-playpause').click();
    } else {
      alert('No other song to play!'); //Will happen on the prev button of the first song.
    }
  });
});