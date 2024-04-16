const content = document.getElementById('content')
var studentId = content.getAttribute('data-class-studentId');
var moduleId = content.getAttribute('data-class-moduleId');
let inputValues = {};
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

            temp.value = inputValues[key].value;
            temp.checked = true;
        }
    
        // Continue with the rest of your code that depends on inputValues
    } catch (error) {
        console.error('Error during data fetching and processing:', error);
    }
    

});
