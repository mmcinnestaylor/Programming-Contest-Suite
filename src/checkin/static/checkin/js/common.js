function swapForm() {
	var email = document.getElementById("emailDiv");
	var swipe = document.getElementById("swipeDiv");
	var button = document.getElementById("formSwap");
	if (email.style.display === "none") {
		swipe.style.display = "none";
		email.style.display = "block";
		button.innerHTML = "Swipe checkin";
	} else {
		swipe.style.display = "block";
		email.style.display = "none";
		button.innerHTML = "Email checkin";
	}
}
