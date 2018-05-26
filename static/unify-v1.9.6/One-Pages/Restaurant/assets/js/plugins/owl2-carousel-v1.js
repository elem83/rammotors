var Owl2Carouselv1 = function () {

	return {

		// Owl Carousel v1
		initOwl2Carouselv1: function () {
			$('.owl2-carousel-v1').owlCarousel({
				responsiveClass: true,
				nav: true,
				navText: ["<span class='glyphicon glyphicon-chevron-left'></span>","<span class='glyphicon glyphicon-chevron-right'></span>"],
				navContainerClass: 'owl-buttons',
				responsive: {
					0:{
						items: 1
					},
					768:{
						items: 1
					},
					992:{
						items: 1
					},
					1200:{
						items: 1
					}
				},
			})
		}

	};

}();
