const btnDiv = document.getElementById('add-question');
const sectionBtn = document.getElementById('add-section');
const courseDiv = document.getElementById('coursediv');
const sectionDiv = document.getElementById('sectiondiv');
const content = document.getElementById('content');
// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'flex';
    content.style.display = 'none';
});

sectionBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    sectionDiv.style.display = 'flex';
    content.style.display = 'none';
});

const closeBtn = document.getElementById('cancel');

closeBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'none';
    content.style.display = 'flex';
});

const closeSectionBtn = document.getElementById('cancel-section');

closeSectionBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    sectionDiv.style.display = 'none';
    content.style.display = 'flex';
});

const filenameSpan = document.getElementById('filename');
const upload = document.getElementById('upload');
upload.addEventListener('change', function () {
    if (upload.files.length > 0) {
        filenameSpan.innerHTML += upload.files[0].name + "<br>";
    }
});