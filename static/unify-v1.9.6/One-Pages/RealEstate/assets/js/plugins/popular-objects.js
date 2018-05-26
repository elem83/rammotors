$(function() {
  $('.popular-objects-list').owlCarousel({
    loop: true,
    margin: 30,
    responsive: {
      0:{
        items: 1
      },
      500:{
        items: 2
      },
      800:{
        items: 3
      },
      992:{
        items: 4
      },
      1250:{
        items: 5
      }
    },
    nav: false,
    dots: false,
  });
});