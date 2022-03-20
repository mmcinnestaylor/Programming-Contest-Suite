// Toggles between email and swipe checkin elements
function swap_form() {
	var email = document.getElementById("emailDiv");
	var swipe = document.getElementById("swipeDiv");
	var button = document.getElementById("formSwap");

	if (email.style.display === "none") {
		swipe.style.display = "none";
		email.style.display = "block";
		document.getElementById("id_email").focus();
		button.innerHTML = "Swipe check-in";
	} 
	else {
		swipe.style.display = "block";
		email.style.display = "none";
		document.getElementById("id_fsu_num").focus();
		button.innerHTML = "Email check-in";
	}
}

// Displays walkin contestant prompt followed by swipe form
function walkin_prompt(is_walkin) {
	var walkin = document.getElementById("walkinDiv");
	var checkin = document.getElementById("checkinDiv");
	var prompt = document.getElementById("walkin_prompt");

	if (is_walkin) {
		walkin.style.display = "block";
	}
	else {
		show_swipe();
	}

	prompt.style.display = "none";
	checkin.style.display = "block";
	document.getElementById("id_fsu_num").focus();
}	

// Display Next button after walk-in division selection
function show_next() {
	var nextButton = document.getElementById("walkinNext");
	nextButton.style.display = "inline";
}

// Display swipe field after of completion of walk-in portion
function show_swipe() {
	var walkin = document.getElementById("walkinDiv");
	var nextButton = document.getElementById("walkinNext");
	var swipe = document.getElementById("swipeDiv");
	var swapButton = document.getElementById("formSwap");

	walkin.style.display = "none";
	nextButton.style.display = "none";
	swipe.style.display = "block";
	swapButton.style.display = "inline";
	swapButton.innerHTML = "Email check-in";
	document.getElementById("id_fsu_num").focus();
}

// Looks for ? sentinal character or press of the enter key
// Submits swipe form input on hit
function read_swipe() {
	var inputarea = document.getElementById("id_fsu_num");

	inputarea.addEventListener("input", function () {
		if (inputarea.value.slice(-1) == "?") {
			document.getElementById("checkinForm").submit();
		}
	});

	inputarea.addEventListener("keyup", function(event) {
		if (event.key === "Enter") {
			document.getElementById("checkinForm").submit();
		}
	  });    
}