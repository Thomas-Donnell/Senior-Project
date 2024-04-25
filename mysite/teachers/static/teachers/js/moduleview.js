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

const filenameContainer = document.querySelector('.filename-wrapper')
const upload = document.getElementById('upload');
let fileList = new DataTransfer();
upload.addEventListener('change', function () {
    if (upload.files.length > 0) {
        for( let i = 0; i < upload.files.length; i++){
            console.log(i)
            console.log(upload.files[i].name)
            const buttonContainer = document.createElement("div");
            buttonContainer.classList.add("buttonContainer");
            var fileName = document.createElement('span')
            fileName.innerHTML = upload.files[i].name
            var deleteButton = document.createElement("div");
            deleteButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="1.75em" height="1.75em" viewBox="0 0 24 24"><path fill="currentColor" d="M7 4a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2h4a1 1 0 1 1 0 2h-1.069l-.867 12.142A2 2 0 0 1 17.069 22H6.93a2 2 0 0 1-1.995-1.858L4.07 8H3a1 1 0 0 1 0-2h4zm2 2h6V4H9zM6.074 8l.857 12H17.07l.857-12zM10 10a1 1 0 0 1 1 1v6a1 1 0 1 1-2 0v-6a1 1 0 0 1 1-1m4 0a1 1 0 0 1 1 1v6a1 1 0 1 1-2 0v-6a1 1 0 0 1 1-1" /></svg>';
 
            const file = upload.files[i];
            let newName = file.name;
            let filenameParts =  file.name.split('.');
            if(filenameParts.length >= 2){
                newName = `${filenameParts[0]}(${fileList.items.length}).${filenameParts[1]}`;
            }
            console.log(newName);
            const newFile = new File([file], newName, { type: file.type });
            fileList.items.add(newFile);

            buttonContainer.appendChild(fileName)
            buttonContainer.appendChild(deleteButton)
            filenameContainer.appendChild(buttonContainer)
            deleteButton.addEventListener('click', function () {
                console.log(newName)
                deleteAttachedImage(newName);
                buttonContainer.remove();
            });
        }
        upload.files = fileList.files;
        console.log(upload.files);

        
    }
});

function deleteAttachedImage(name){
    if (upload.files.length > 0) {
        let fileListRemove = new DataTransfer();
        for( let i = 0; i < upload.files.length; i++){
            if (upload.files[i].name !== name) { // Exclude file at index 1 (second file) from the new FileList
                fileListRemove.items.add(upload.files[i]);
            }
        }
        fileList = fileListRemove;
        upload.files = fileListRemove.files;
        console.log(upload.files);
    }
}

const imageUrl = document.getElementById('imageUrl');
const images = document.querySelectorAll('.images');
let selectedImages = new Set();
// Add a click event listener to each div
images.forEach(function(image) {
    const buttonContainer = document.createElement("div");
    const deleteButton = document.createElement("div");
    const fileName = document.createElement('span')
    image.addEventListener('click', function() {
        // Your event handling code here
        let selectedImageUrl = image.src;
        const segments = selectedImageUrl.split("/");
        selectedImageUrl = segments[segments.length - 1];

        console.log(selectedImageUrl);
        if(selectedImages.has(image)){
            image.classList.toggle('image');
            selectedImages.delete(image);
            deleteButton.remove();
            fileName.remove();
            buttonContainer.remove();
        }else{
            image.classList.toggle('image');
            buttonContainer.classList.add("buttonContainer");
            fileName.innerHTML = selectedImageUrl
            deleteButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="1.75em" height="1.75em" viewBox="0 0 24 24"><path fill="currentColor" d="M7 4a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2h4a1 1 0 1 1 0 2h-1.069l-.867 12.142A2 2 0 0 1 17.069 22H6.93a2 2 0 0 1-1.995-1.858L4.07 8H3a1 1 0 0 1 0-2h4zm2 2h6V4H9zM6.074 8l.857 12H17.07l.857-12zM10 10a1 1 0 0 1 1 1v6a1 1 0 1 1-2 0v-6a1 1 0 0 1 1-1m4 0a1 1 0 0 1 1 1v6a1 1 0 1 1-2 0v-6a1 1 0 0 1 1-1" /></svg>';
            buttonContainer.appendChild(fileName)
            buttonContainer.appendChild(deleteButton)
            filenameContainer.appendChild(buttonContainer)
            selectedImages.add(image)
            deleteButton.addEventListener('click', function () {
                selectedImages.delete(image);
                deleteButton.remove();
                fileName.remove();
                buttonContainer.remove();
            });
        }
        
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

const sectionForm = document.getElementById('sectionForm');
const sectionSubmit = document.getElementById('sectionSubmit');

sectionSubmit.addEventListener('click', function () {
    sectionForm.submit(); // Submit the form when the button is clicked
});