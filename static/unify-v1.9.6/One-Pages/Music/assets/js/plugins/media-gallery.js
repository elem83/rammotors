$(function() {
  function mySwiperF() {
    var mySwiper = new Swiper ('.swiper-container', {
      pagination: '.swiper-pagination',
      slidesPerView: 6,
      slidesPerColumn: 2,
      spaceBetween: 30,
      paginationClickable: true,
      breakpoints: {
        // when window width is <= 991px
        2000: {
          slidesPerView: 6,
        },
        // when window width is <= 991px
        991: {
          slidesPerView: 5,
        },
        // when window width is <= 767px
        767: {
          slidesPerView: 4,
        },
        // when window width is <= 599px
        599: {
          slidesPerView: 3,
        },
        // when window width is <= 499px
        499: {
          slidesPerView: 2,
        },
        // when window width is <= 399px
        399: {
          slidesPerView: 1,
        },
      }
    });
  }
  mySwiperF();
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    e.target;
    e.relatedTarget;
    mySwiperF();
  })
});