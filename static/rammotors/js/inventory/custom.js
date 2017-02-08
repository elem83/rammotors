$(document).ready(function(){
  $( "input[name='optionsRadios']" ).prop('checked', false);

  var brand;

  $('input[type=checkbox]').change(
    function(){
      $('input[type=checkbox]').each(function () {
        if (this.checked) {
            brand = $(this).val();
            $('div[name='+ brand +']').show("slow");
        } else {
            brand = $(this).val();
            $('div[name='+ brand +']').hide("slow");
        }
      });
  });

  $('#reset').click(function(){
    $('input[type=checkbox]').each(function () {
      $(this).attr('checked', false);
      brand = $(this).val();
      $('div[name='+ brand +']').show("slow");
    });
  });

});// end of document ready
