document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];
        return cookieValue;
    }
    const csrfToken = getCSRFToken();

    // Add a click event listener to each div
    buttons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const listItem = event.target.closest(".list-item");
            const inputField = listItem.querySelector('.textarea-input');
            let shortAnswerId = button.getAttribute('data-short-answer')
            var grade = inputField.value;       
            fetch('/teachers/grade_submission/' + shortAnswerId + '/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ grade: grade}),
            })
            .then(response => {
                if(response.ok){
                    console.log("success")
                }else{
                    console.log("error");
                }
                
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });

            listItem.remove()

        });
    });
    

});