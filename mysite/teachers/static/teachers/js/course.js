const btnDiv = document.getElementById('addstudents');
const deleteDiv = document.getElementById('delete');
const gradeDiv = document.getElementById('grades-link');
const courseGradesDiv = document.getElementById('coursediv-grades');
const courseDiv = document.getElementById('coursediv');
const tagWrapper = document.getElementById('tagwrapper');
const alertDiv = document.getElementById('coursediv-alert')

// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    tagWrapper.style.display = 'none';
    courseDiv.style.display = 'flex';
});

deleteDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    content.style.display = 'none';
    alertDiv.style.display = 'flex';
});

gradeDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseGradesDiv.style.display = 'flex';
    content.style.display = 'none';
});

const closeBtns = document.querySelectorAll('.close');

closeBtns.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        courseGradesDiv.style.display = 'none';
        alertDiv.style.display = 'none';
        content.style.display = 'block';
    });
});

const divs = document.querySelectorAll('.grades');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        courseId = div.getAttribute('data-class-courseId');
        studentId = div.getAttribute('data-class-studentId');
        window.location.href = `/teachers/student_view/${courseId}/${studentId}/`;
    });
});

function sortStudents() {
    var sortOrderSelect = document.getElementById('sortOrder');
    var sortOrder = sortOrderSelect.value;

    var gradesWrapper = document.getElementById('grades-wrapper');
    var grades = Array.from(gradesWrapper.getElementsByClassName('grades'));

    grades.sort(function (a, b) {
        var gradeA = parseFloat(a.children[1].innerText);
        var gradeB = parseFloat(b.children[1].innerText);

        if (sortOrder === 'asc') {
            return gradeA - gradeB;
        } else {
            return gradeB - gradeA;
        }
    });

    // Clear the grades wrapper
    gradesWrapper.innerHTML = '';

    // Append sorted grades back to the grades wrapper
    grades.forEach(function (grade) {
        gradesWrapper.appendChild(grade);
    });
}