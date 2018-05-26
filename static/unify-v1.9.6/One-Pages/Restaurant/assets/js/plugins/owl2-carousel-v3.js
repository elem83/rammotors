var Owl2Carouselv3 = function () {
	return {
		// Owl Carousel v3
		initOwl2Carouselv3: function () {
			$('.owl2-carousel-v3').owlCarousel({
				margin: 30,
				loop: true,
				items: 4,
				responsiveClass: true,
				nav: true,
				navText: ["<span class='glyphicon glyphicon-chevron-left'></span>","<span class='glyphicon glyphicon-chevron-right'></span>"],
				navContainerClass: 'owl-buttons',
				dots:true,
				dotsClass: 'owl-pagination',
				dotClass: 'owl-page',
		    responsive: {
	        1200:{
            items: 4,
	        },
	        768:{
            items: 3,
	        },
	        520:{
            items: 2,
	        },
	        430:{
            items: 1,
	        }
	    	}
			})
		}
	};
}();


