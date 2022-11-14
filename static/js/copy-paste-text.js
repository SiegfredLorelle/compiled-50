// Make all copy buttons to listen to clicks which copies its sibling as clipboard then alert user 
// Input for key
const TextInput = document.querySelector("#text")

// Select all copy button and loop through each button 
document.querySelectorAll("#copy-btn-text").forEach(button => {
    
    // Add Event Listener on click 
    button.addEventListener('click', () => {

        // Copy the card number beside it and copy it to clipboard 
        const copyText = button.previousElementSibling.innerHTML;
        navigator.clipboard.writeText(copyText).then(() => {

            // Put the copied key in input then focus on it
            TextInput.value = copyText;
            TextInput.focus()

            // Inform users that the text is copied and pasted on the input
            alert(`${copyText} is copied and pasted to text input.`);
        });
    })
})
