const backDiv = document.getElementById('backbtn');

// Add a click event listener to the trigger div
backDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    window.history.back();
});