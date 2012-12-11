
/**
 * Code JS Instituts
 */
$(document).ready(function(){
	function theCarousel(carousel)
	{
		jQuery('.jcarousel-control a').bind('mouseover', function() { 
			carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
			carousel.stopAuto();
			return false;
		});
		jQuery('.jcarousel-control a').bind('mouseout', function() { 
			carousel.startAuto();
			return false;
		});
		
		carousel.clip.hover(function() {
			carousel.stopAuto();
		}, function() {
			carousel.startAuto();
		});
		
	}
	$('#content').jcarousel({ scroll: 1, auto: 6, wrap: 'last', buttonPrevHTML: false, buttonNextHTML: false, initCallback: theCarousel });
});


/**
 * Fonction qui sert a reduire le letter-spacinf sur Firefox sous LINUX sur la page d'accueil
 */
/*
$(document).ready(function(){
	if($.browser.OS=="Linux"){//seulement pour Mozilla compatible
		$("#rightLeft ul li a").css("letter-spacing","-1px");
	}
});*/

$(document).ready(function(){ 
	$("#rightLeft ul li").hover(function () {
      $(this).css({ background:"#FFFFFF url(squelettes/styles/images/bg-lien2.gif)"});
    }, function () {
      var cssObj = {
        background: "#FFFFFF url(squelettes/styles/images/bg-lien.gif)"
      }
      $(this).css(cssObj);
    });
});

$(document).ready(function(){ 
	$(".hover").hover(function () {
      $(this).css({ backgroundColor:"#d0d0d3"});
    }, function () {
      var cssObj = {
        backgroundColor: "#e9eaea"
      }
      $(this).css(cssObj);
    });
});

