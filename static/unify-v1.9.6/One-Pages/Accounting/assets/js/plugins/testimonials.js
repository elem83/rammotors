$(function() {
  $('.testinomials-nav').on('click', '.slick-slide', function (e) {
    e.stopPropagation();
    var index = $(this).data('slick-index');
    if ($('.testinomials-nav').slick('slickCurrentSlide') !== index) {
      $('.testinomials-nav').slick('slickGoTo', index);
    }
  });
  $('.testinomials-nav').slick({
    centerMode: true,
    slidesToShow: 5,
    asNavFor: '.testinomials-content',
    infinite: true,
    arrows: false,
    // responsive: [
    //   {
    //     breakpoint: 767,
    //     settings: {
    //       slidesToShow: 3,
    //     }
    //   },
    //   {
    //     breakpoint: 480,
    //     settings: {
    //       slidesToShow: 1
    //     }
    //   }
    // ]
  });

  $('.testinomials-content').slick({
    slidesToShow: 1,
    infinite: true,
    arrows: false,
    asNavFor: '.testinomials-nav',
    dots: true,
  });
});