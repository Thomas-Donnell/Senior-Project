const divs = document.querySelectorAll('.quizes');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        id = div.getAttribute('data-class-id');
        courseId = div.getAttribute('data-class-courseId');
        window.location.href = `/students/quiz_view/${id}/${courseId}/`;
    });
});