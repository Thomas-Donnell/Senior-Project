// Get references to the trigger and target divs
const btnDiv = document.getElementById('addbtn');
const courseDiv = document.getElementById('coursediv');
const content = document.getElementById('content');
// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'flex';
    content.style.display = 'none';
});

const divs = document.querySelectorAll('.posts');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        id = div.getAttribute('data-class-id');
        courseId = div.getAttribute('data-class-courseId');
        window.location.href = `/teachers/post/${id}/${courseId}/`;
    });
});
const filenameSpan = document.getElementById('filename');
const upload = document.getElementById('upload');
upload.addEventListener('change', function () {
    if (upload.files.length > 0) {
        filenameSpan.innerHTML += upload.files[0].name + "<br>";
    }
});