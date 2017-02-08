$(document).ready(function(){
  $( "input[name='optionsRadios']" ).prop('checked', false);

  // Isotop

  var $grid = $('.grid').isotope({
    itemSelector: '.col-md-4',
    layoutMode: 'fitRows'
  });

  var $list = $('.list').isotope({
    itemSelector: '.list-product-description',
    layoutMode: 'fitRows'
  });

  // bind filter button click
  $('#filters').on( 'click', "input[name='optionsRadios']", function() {
    var filterValue = $( this ).attr('data-filter');
    $grid.isotope({ filter: filterValue });
    $list.isotope({ filter: filterValue });
  });
});// end of document ready
