/* Track the mouse movement then adjust width of left side based on mouse position */

// Left side (color black)
const left = document.getElementById("left-side");

// Change the width of left side based on mouse movement
const handleOnMove = e => {
    const p = e.clientX / window.innerWidth * 100;

    left.style.width = `${p}%`;
}

// Track mouse movement
document.onmousemove = e => handleOnMove(e);

// Track touch (for mobile)
document.ontouchmove = e => handleOnMove(e.touches[0]);
