
const btnDiv = document.getElementById('reply-btn');
const courseDiv = document.getElementById('coursediv');
const postWrapper = document.getElementById('wrapper');
// Add a click event listener to the trigger divß
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'flex';
    postWrapper.style.display = 'none';
});


const deleteBtn = document.getElementById('delete-btn');
deleteBtn.addEventListener('click', function() {
    courseId = deleteBtn.getAttribute('data-class-courseId');
    id = deleteBtn.getAttribute('data-class-id');
    window.location.href = `/teachers/delete_post/${id}/${courseId}/`;
});