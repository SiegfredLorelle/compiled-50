// Make all copy buttons to listen to clicks which copies its sibling as clipboard then alert user 
// Input for key
const input = document.querySelector("#key")

// Select all copy button and loop through each button 
document.querySelectorAll("#copy-btn-bg").forEach(button => {
    
    // Add Event Listener on click 
    button.addEventListener('click', () => {

        // Copy the card number beside it and copy it to clipboard 
        const copyText = button.previousElementSibling.innerHTML;
        navigator.clipboard.writeText(copyText).then(() => {

            // Inform users that the text is copied and pasted on the input
            alert(`${copyText} is copied to clipboard!`);
        });
    })
})
