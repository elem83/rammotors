var Owl2Carouselv4 = function () {
	return {
		// Owl Carousel v4
		initOwl2Carouselv4: function () {
			$('.owl2-carousel-v4').owlCarousel({
				// margin: 1,
				loop: true,
				margin: 25,
				responsiveClass: true,
				nav: true,
				dots: false,
				navText: ["<span class='glyphicon glyphicon-chevron-left'></span>","<span class='glyphicon glyphicon-chevron-right'></span>"],
				navContainerClass: 'owl-buttons',
		    responsive: {
					0:{
						items: 1
					},
					550:{
						items: 2
					},
					992:{
						items: 3
					},
					1200:{
						items: 4
					},
					1300:{
						items: 4
					}
				}
			})
		}
	};
}();


