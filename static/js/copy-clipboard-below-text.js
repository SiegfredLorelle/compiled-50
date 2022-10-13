// Make all copy buttons to listen to clicks which copies its child as clipboard then alert user 

// Select all copy button and loop through each button 
document.querySelectorAll("#copy-button").forEach(button => {
    
    // Add Event Listener on click 
    button.addEventListener('click', () => {

        // Copy the paragraph below it and copy it to clipboard 
        const copyText = button.parentElement.nextElementSibling.innerHTML;
        navigator.clipboard.writeText(copyText).then(() => {

            // Warn users that the text is copied
            alert(`Paragraph copied to clipboard!` );
        });
    })
})
