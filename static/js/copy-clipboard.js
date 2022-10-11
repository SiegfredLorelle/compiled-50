// Make all copy buttons to listen to clicks which copies its sibling as clipboard then alert user 

// Select all copy button and loop through each button 
document.querySelectorAll("#copy-button").forEach(button => {
    
    // Add Event Listener on click 
    button.addEventListener('click', () => {

        // Copy the card number beside it and copy it to clipboard 
        const copyText = button.previousElementSibling.innerHTML;
        navigator.clipboard.writeText(copyText).then(() => {

            // Warn users that the text is copied
            alert(`${copyText} is copied to clipboard!` );
        });
    })
})
