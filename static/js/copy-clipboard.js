// Make all copy buttons to listen to clicks which copies its sibling as clipboard then alert user 

document.querySelectorAll("#copy-button").forEach(item => {
    item.addEventListener('click', () => {
        alert(item.previousElementSibling.innerHTML)
    })
})
