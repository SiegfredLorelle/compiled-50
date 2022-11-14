// Make all copy buttons to listen to clicks which copies its child as clipboard then alert user 


// Input for paragraph
let input = document.querySelector("#paragraph")

// Select all copy button and loop through each button 
document.querySelectorAll("#copy-btn-bg").forEach(button => {
    
    // Add Event Listener on click 
    button.addEventListener('click', () => {

        // Copy the paragraph below it and copy it to clipboard 
        const copyText = button.parentElement.nextElementSibling.innerHTML;
        navigator.clipboard.writeText(copyText).then(() => {

            // Put the copied paragraph in input then focus on it
            input.value = copyText;
            input.focus()

            // Warn users that the text is copied
            alert(`Paragraph is copied and will be pasted to paragraph box!` );
        });
    })
})
