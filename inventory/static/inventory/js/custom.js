$(document).ready(function(){
  $( "input[name='optionsRadios']" ).prop('checked', false);
  var count_original = $('#count_car').html();

  // init Isotope
  var $grid = $('.grid').isotope({
    itemSelector: '.col-md-4',
    layoutMode: 'fitRows',
    getSortData: {
      km: function( itemElem ) { // function
            var km = $( itemElem ).find('.km').text();
            return parseFloat(km.replace(',', '').replace( /[\(\)]/g, ''));
      },
      price: function( itemElem ) { // function
            var price = $( itemElem ).find('.price').text();
            return parseFloat(price.replace(',', '').replace( /[\(\)]/g, ''));
      }
    }
  });

  var $list = $('.list').isotope({
    itemSelector: '.list-product-description',
    layoutMode: 'vertical',
    getSortData: {
      km: function( itemElem ) { // function
            var km = $( itemElem ).find('.km').text();
            return parseFloat(km.replace(',', '').replace( /[\(\)]/g, ''));
      },
      price: function( itemElem ) { // function
            var price = $( itemElem ).find('.price').text();
            return parseFloat(price.replace(',', '').replace( /[\(\)]/g, ''));
      }
    }
  });

  // bind filter button click
  $('#filters').on( 'click', "input[name='optionsRadios']", function() {
    var filterValue = $( this ).attr('data-filter');
    var count = $(this).attr('data-count');
    $('#count_car').html(count);
    if (count == 1) {
      $('#pluralize_count_car').html('')
    } else {
      $('#pluralize_count_car').html('s');
    }
    $grid.isotope({ filter: filterValue });
    $list.isotope({ filter: filterValue });
  });

  $('#reset').click(function() {
    var filterValue = $( this ).attr('data-filter');
    $grid.isotope({ filter: filterValue });
    $list.isotope({ filter: filterValue });
    $( "input[name='optionsRadios']" ).prop('checked', false);
    $('#count_car').html(count_original);
  });

  // bind sort button click
  $('#sorts').on( 'click', 'li', function() {
    var sortByValue = $(this).attr('data-sort-by');
    $grid.isotope({ sortBy: sortByValue });
    $list.isotope({ sortBy: sortByValue });
  });

  $("#sorts").on( 'click', 'li', function(event) {
    event.preventDefault();
    var href = $(this).html();
    var sort_criteria = $(href).text();
    $('#sort_criteria').html(sort_criteria + "<span class='caret'></span>")
  });

});// end of document ready
