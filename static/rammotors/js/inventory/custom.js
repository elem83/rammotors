$(document).ready(function(){
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

});// end of document ready
