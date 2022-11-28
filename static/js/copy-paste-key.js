/* Make all copy buttons to listen to clicks then
copy key beside the btn then paste to key input box */

// Input for key
const keyInput = document.querySelector("#key");

// Select all copy button and loop through each button 
document.querySelectorAll("#copy-btn-bg").forEach(button => {
    
    // Add Event Listener on click 
    button.addEventListener('click', () => {

        // Copy the card number beside it and copy it to clipboard 
        const copyKey = button.previousElementSibling.innerHTML;
        navigator.clipboard.writeText(copyKey).then(() => {

            // Put the copied key in input then focus on it
            keyInput.value = copyKey;
            keyInput.focus();

            // Inform users that the text is copied and pasted on the input
            alert(`${copyKey} is copied and pasted to key input.`);
        });
    });
});
