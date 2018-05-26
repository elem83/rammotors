$(function() {
  var PromoSlider = new MasterSlider();
  PromoSlider.setup('masterslider-promo' , {
	  width: 1400,    // PromoSlider standard width
	  height: 1800,   // PromoSlider standard height
	  speed: 70,
	  layout: 'fullscreen',
	  loop: true,
	  preload: 0,
	  autoplay: false,
	  layersMode: 'center',
  });
  // adds Arrows navigation control to the PromoSlider.
  // PromoSlider.control('arrows', {autohide:false});
  PromoSlider.control('lightbox');
  PromoSlider.control('thumblist' , {autohide:false ,
  	dir:'h',
  	align:'top',
		width:550,
		height:50,
		margin:0,
		space:0 ,
		hideUnder:500,
		type:'tabs',
		inset: true

  	});
});
