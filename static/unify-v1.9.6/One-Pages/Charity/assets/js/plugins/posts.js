$(function() {
  $('.posts').slick({
    centerMode: true,
    arrows: false,
    slidesToShow: 3,
    centerPadding: '0',
    variableWidth: true,
    responsive: [
      {
        breakpoint: 1200,
        settings: {
          slidesToShow: 1,
        }
      },
      // {
      //   breakpoint: 767,
      //   settings: {
      //     centerMode: false,
      //   }
      // }
    ]
  });
});