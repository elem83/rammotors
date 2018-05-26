$(function() {
  $('.important-objects-list').slick({
    centerMode: true,
    arrows: true,
    dots: true,
    slidesToShow: 3,
    variableWidth: true,
    prevArrow: '<div class="slick-prev"><i class="fa fa-angle-left"></i></div>',
    nextArrow: '<div class="slick-next"><i class="fa fa-angle-right"></i></div>',
    responsive: [
      {
        breakpoint: 970,
        settings: {
          slidesToShow: 1,
          variableWidth: false,
        }
      },
      {
        breakpoint: 500,
        settings: {
          centerMode: false,
        }
      }
    ]
  });
});