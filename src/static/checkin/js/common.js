function swapForm() {
	var x = document.getElementById("emailDiv");
	var y = document.getElementById("swipeDiv");
	if (x.style.display === "none") {
		y.style.display = "none";
		x.style.display = "block";
	} else {
		y.style.display = "block";
		x.style.display = "none";
	}
}
