function swap_form() {
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

function walkin_prompt(is_walkin) {
	var walkin = document.getElementById("walkinDiv");
	var checkin = document.getElementById("checkin_form");
	var prompt = document.getElementById("walkin_prompt");

	if (is_walkin) {
		walkin.style.display = "block";
	}

	prompt.style.display = "none";
	checkin.style.display = "block";
}
