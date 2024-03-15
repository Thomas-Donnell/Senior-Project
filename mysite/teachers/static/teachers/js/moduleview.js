const actionWrapper = document.getElementById('actionWrapper');
const btnDiv = document.getElementById('add-question');
const sectionBtn = document.getElementById('add-section');
const courseDiv = document.getElementById('coursediv');
const sectionDiv = document.getElementById('sectiondiv');
const prefabWrapper = document.getElementById('prefabWrapper');
const prefabBtn = document.getElementById('prefabContainer');
const content = document.getElementById('contentwrapper');
// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    actionWrapper.style.display = 'block';
    courseDiv.style.display = 'flex';
    content.style.display = 'none';
});

prefabBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    if (prefabWrapper.style.display === 'flex') {
        // If currently displayed, hide it
        prefabWrapper.style.display = 'none';
    } else {
        // If currently hidden, show it as a flex container
        prefabWrapper.style.display = 'flex';
    }

    prefabBtn.classList.toggle('blue');
});

sectionBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    actionWrapper.style.display = 'block';
    sectionDiv.style.display = 'flex';
    content.style.display = 'none';
});

const closeBtn = document.getElementById('cancel');

closeBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    actionWrapper.style.display = 'none';
    courseDiv.style.display = 'none';
    content.style.display = 'flex';
});

const closeSectionBtn = document.getElementById('cancel-section');

closeSectionBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    actionWrapper.style.display = 'none';
    sectionDiv.style.display = 'none';
    content.style.display = 'flex';
});

const filenameSpan = document.getElementById('filename');
const upload = document.getElementById('upload');
upload.addEventListener('change', function () {
    if (upload.files.length > 0) {
        filenameSpan.innerHTML = upload.files[0].name + "<br>";
    }
});

const imageUrl = document.getElementById('imageUrl');
const images = document.querySelectorAll('.images');
let selectedImage = null;
// Add a click event listener to each div
images.forEach(function(image) {
    image.addEventListener('click', function() {
        // Your event handling code here
        if(selectedImage !== null){
            selectedImage.classList.toggle('image');
        }
        selectedImage = image;
        selectedImage.classList.toggle('image');
        
        let selectedImageUrl = selectedImage.src;
        const segments = selectedImageUrl.split("/");
        selectedImageUrl = segments[segments.length - 1];

        console.log(selectedImageUrl);
        imageUrl.value = selectedImageUrl;
        filenameSpan.innerHTML = selectedImageUrl + "<br>";
    });
});