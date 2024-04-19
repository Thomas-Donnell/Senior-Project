const content = document.getElementById('content')
const newSubmission = document.getElementById('new-submission');
const wrapper = document.getElementById('wrapper');
const gradeWrapper = document.getElementById('grade-wrapper');
var studentId = content.getAttribute('data-class-studentId');
var moduleId = content.getAttribute('data-class-moduleId');
let inputValues = {};
let progress = 0;

newSubmission.addEventListener('click', function() {
    gradeWrapper.style.display = 'none';
    wrapper.style.display = 'block';
});

function getModuleData(){
    return new Promise((resolve, reject) => {
        fetch('/teachers/module_data/' + studentId + '/' + moduleId + '/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            inputValues = data.input_values;
            progress = data.progress;
            resolve();
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            reject(error);
        });
    });
}


// Wait for the DOMContentLoaded event before executing JavaScript
document.addEventListener('DOMContentLoaded', async function() {
    // Get all input elements with the "dynamicInput" class
    const inputElements = document.querySelectorAll('.dynamicInput');

    try {
        await getModuleData(); // Wait for getModuleData to complete
        // Variable to store input values with names and IDs
        for(let key in inputValues){
            var temp = null;
            if(inputValues[key].type == 'radio'){
                temp = document.querySelector(`[name="${key}"][value="${inputValues[key].value}"]`);
            }else{
                temp = document.querySelector(`[name="${key}"]`);
            }
            if(temp === null){
                delete inputValues[key];
            }else{
                temp.value = inputValues[key].value;
                temp.checked = true;
            }

        }
        if(inputValues === null){
            inputValues = {};
        }
        
        // Add event listeners to each input element
        inputElements.forEach(input => {
            // Add event listener for "input" event on each input element
            input.addEventListener('input', function() {
                // Update the inputValues object with the new input value, name, and ID
                inputValues[input.name] = {'value':input.value, 'type':input.type};
                if(input.value == ""){
                    delete inputValues[input.name];
                }
                var length = Object.keys(inputValues).length;
                progress = (length/inputElements.length) * 100;
            });
        });
        // Continue with the rest of your code that depends on inputValues
    } catch (error) {
        console.error('Error during data fetching and processing:', error);
    }
    

});

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}
const csrfToken = getCSRFToken();

function sendInputValues() {
    return new Promise((resolve, reject) => {
        fetch('/teachers/module_data/' + studentId + '/' + moduleId + '/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ input_values: inputValues, progress: progress }),
        })
        .then(response => {
            if(response.ok){
                resolve(data);
            }else{
                reject(error);
            }
            
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            reject(error);
        });
    });
}

window.addEventListener('beforeunload', async function (e) {

    try {
        // Trigger the function to send input values
        const responseData = await sendInputValues();
        console.log('Response data:', responseData);

    } catch (error) {
        console.error('Error sending input values:', error);
    }
});
