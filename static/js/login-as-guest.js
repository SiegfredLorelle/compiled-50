// Log the user as guest automatically

// Get the btns and inputs
const loginAsGuestBtn = document.querySelector("#login-as-guest-btn");
const loginBtn = document.querySelector("#login")
const username = document.querySelector("#username");
const password = document.querySelector("#password");

const guest = "guest";

// On clicking log in as guest btn
loginAsGuestBtn.addEventListener("click", function() {

    // Reprompt if sure to log in as guest 
    if (confirm("Are you sure to log in as guest?")) {


        // Type the login details of guest
        username.value = guest
        password.value = guest

        // Click the login btn
        loginBtn.click()
    }
});


// Select all copy button and loop through each button 
