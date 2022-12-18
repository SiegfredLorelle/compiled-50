/* Inform user via alert that the message was sent */

// Get submit button
const submit_btn = document.querySelector("#msg-submit-btn");
// Alert message sent when submit button is clicked
submit_btn.addEventListener("click", () => {
  alert("Message has been sent!");
});