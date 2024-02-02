const submitBtn = document.getElementById('submitbtn');
const newSubmission = document.getElementById('new-submission');
const wrapper = document.getElementById('wrapper');
const gradeWrapper = document.getElementById('grade-wrapper');
const form = document.getElementById('form');
// Add a click event listener to the trigger div
submitBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    form.submit()
});

newSubmission.addEventListener('click', function() {
    gradeWrapper.style.display = 'none';
    wrapper.style.display = 'block';
});