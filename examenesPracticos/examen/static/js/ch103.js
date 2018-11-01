

(function() {
    // Loading the Google Maps API
    var latLng = {lat:19.5436299 , lng: -96.9266971};
    var geocoder;
    var loc;
    window.onload = function() {
	var mapCanvas = document.getElementById('map-canvas');
	var mapOptions = {
	    center: new google.maps.LatLng(19.5436299, -96.9266971),
	    zoom: 15,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
    }
var map = new google.maps.Map(mapCanvas, mapOptions);
	    var marker = new google.maps.Marker({
		position: latLng,
		map: map
});

    }
})();


