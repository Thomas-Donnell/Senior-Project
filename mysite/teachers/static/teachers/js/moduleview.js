const actionWrapper = document.getElementById('actionWrapper');
const btnDiv = document.getElementById('add-question');
const sectionBtn = document.getElementById('add-section');
const courseDiv = document.getElementById('coursediv');
const sectionDiv = document.getElementById('sectiondiv');
const prefabWrapper = document.getElementById('prefabWrapper');
const multiChoiceBtn = document.getElementById('multiple-choice-button');
const shortAnsBtn = document.getElementById('short-answer-button');
const shortAnsForm = document.getElementById('short-answer-form');
const multiChoiceForm = document.getElementById('multiple-choice-form');
const prefabBtn = document.getElementById('prefabContainer');
const templateBtn = document.getElementById('templateContainer');
const content = document.getElementById('contentwrapper');
// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    actionWrapper.style.display = 'block';
    courseDiv.style.display = 'flex';
    content.style.display = 'none';
});

multiChoiceBtn.addEventListener('click', function() {
    shortAnsForm.style.display = 'none';
    multiChoiceForm.style.display = 'block';
})

shortAnsBtn.addEventListener('click', function() {
    multiChoiceForm.style.display = 'none';
    shortAnsForm.style.display = 'block';
})

templateBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    if (templateWrapper.style.display === 'flex') {
        // If currently displayed, hide it
        templateWrapper.style.display = 'none';
    } else {
        // If currently hidden, show it as a flex container
        templateWrapper.style.display = 'flex';
        prefabWrapper.style.display = 'none';
        prefabBtn.classList.remove('blue');
    }

    templateBtn.classList.toggle('blue');
});

prefabBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    if (prefabWrapper.style.display === 'flex') {
        // If currently displayed, hide it
        prefabWrapper.style.display = 'none';
    } else {
        // If currently hidden, show it as a flex container
        prefabWrapper.style.display = 'flex';
        templateWrapper.style.display = 'none';
        templateBtn.classList.remove('blue');
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
    location.reload();
});

const closeShortAnsBtn = document.getElementById('cancel-short-answer');
closeShortAnsBtn.addEventListener('click', function(){
    location.reload();
})

const closeSectionBtn = document.getElementById('cancel-section');

closeSectionBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    location.reload();
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

const defaultModule = document.getElementById('defaultModule');
const templates = document.querySelectorAll('.templates');
let selectedTemplate = null;
templates.forEach(function(template){
    template.addEventListener('click', function(){
        let defaultTemplate = template.getAttribute('data-defaultModule');
        if(selectedTemplate !== null){
            selectedTemplate.classList.toggle('image');
        }
        selectedTemplate = template;
        selectedTemplate.classList.toggle('image');
        defaultModule.value = defaultTemplate
    });
});