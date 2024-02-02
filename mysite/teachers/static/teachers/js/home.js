// Get references to the trigger and target divs
const btnDiv = document.getElementById('addbtn');
const courseDiv = document.getElementById('coursediv');


// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    courseDiv.style.display = 'block';
});

const divs = document.querySelectorAll('.cards');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        courseId = div.getAttribute('data-class-id');
        window.location.href = `course/${courseId}/`;
    });
});

var currentYear = new Date().getFullYear();
var yearDropdown = document.getElementById("id_year");
console.log(currentYear)
for (var i = 0; i < 10; i++) {
    var option = document.createElement("option");
    option.value = currentYear + i;
    option.text = currentYear + i;
    yearDropdown.appendChild(option);
}