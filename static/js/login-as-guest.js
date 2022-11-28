// Log the user as guest automatically

// Input for credit card number
const loginAsGuestBtn = document.querySelector("#login-as-guest-btn");
const loginBtn = document.querySelector("#login")
const username = document.querySelector("#username");
const password = document.querySelector("#password");

const guest = "guest";
loginAsGuestBtn.addEventListener("click", () => 

        // Copy the card number beside it and copy it to clipboard 
        navigator.clipboard.writeText(guest).then(() => {

            // Put the copied credit card numbers in input then focus on it
            username.value = guest
            password.value = guest

            // Inform users that the text is copied and pasted on the input
            alert(`${guest} is copied and will be pasted to credit card number box!`)
            
            loginBtn.click();
        })
)


// Select all copy button and loop through each button 
