



(function() {

    function crearModal(img)
    {
	var modal = document.getElementById('myModal');
    
	var img = document.getElementById(img);
	var modalImg = document.getElementById("img01");
	img.onclick = function(){
	    modal.style.display = "block";
	    modalImg.src = this.src;
	}
    }

    
window.onload = function() {

    crearModal('myImg3');
    crearModal('myImg2');
    crearModal('myImg');
    crearModal('myImg4');
    crearModal('myImg5');
    crearModal('myImg6');
    crearModal('myImg7');
    crearModal('myImg8');
    crearModal('myImg9');
    crearModal('myImg10');
    crearModal('myImg11');
    crearModal('myImg12');
    var modal = document.getElementById('myModal');
// Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
    span.onclick = function() { 
	modal.style.display = "none";
}

}

})();
