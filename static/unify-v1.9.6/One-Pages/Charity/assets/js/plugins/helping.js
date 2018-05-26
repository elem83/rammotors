$(function() {
  $('.helping-list').slick({
    infinite: false,
    arrows: true,
    prevArrow: '<div class="slick-prev"><i class="fa fa-chevron-left"></i></div>',
    nextArrow: '<div class="slick-next"><i class="fa fa-chevron-right"></i></div>',
    slidesToShow: 2,
    responsive: [
      {
        breakpoint: 1199,
        settings: {
          slidesToShow: 1
        }
      },
    ]
  });
});