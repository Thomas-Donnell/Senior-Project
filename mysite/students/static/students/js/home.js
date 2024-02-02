const divs = document.querySelectorAll('.cards');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        courseId = div.getAttribute('data-class-id');
        window.location.href = `course/${courseId}/`;
    });
});