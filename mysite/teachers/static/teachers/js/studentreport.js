const content = document.getElementById('content')
var studentId = content.getAttribute('data-class-studentId');
var labels = [];  // Course names
var dataValues = [];  // Percentiles
var grades = [];  // grades
initialLoad()


function createBarChart(labels, data, chartId) {
    var canvas = document.getElementById(chartId);

    var existingChart = Chart.getChart(canvas);
    if (existingChart) {
        existingChart.destroy();
    }

    var ctx = canvas.getContext('2d');
    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: chartId,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(255, 255, 99, 0.7)',
                    'rgba(99, 255, 132, 0.7)',
                    'rgba(99, 132, 255, 0.7)',
                    'rgba(255, 99, 255, 0.7)',
                ],
            }],
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            // Other options
        }
    });
    return myBarChart;
}
function initialLoad(){
    labels = [];  // Course names
    dataValues = [];  // Percentiles
    grades = [];  // grades

    fetch('/teachers/student_report/' + studentId + '/', {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(grade => {
            labels.push(grade.course_name);
            dataValues.push(grade.percentile);
            grades.push(grade.grades)
        });
    
        createBarChart(labels, dataValues, "percentile");
        createBarChart(labels, grades, "grade");
    })
    .catch(error => console.error('Error fetching data:', error));
}


function changeTerm() {
    labels = [];  // Course names
    dataValues = [];  // Percentiles
    grades = [];  // grades
    var changeTerm = document.getElementById('changeTerm');
    var term = changeTerm.value;
    if(term == 'current'){
        initialLoad()
    }
    else{
        fetch('/teachers/past_semester/' + studentId + '/' + term + '/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            data.forEach(grade => {
                labels.push(grade.course_name);
                dataValues.push(grade.percentile);
                grades.push(grade.grades)
            });
        
            createBarChart(labels, dataValues, "percentile");
            createBarChart(labels, grades, "grade");
        })
        .catch(error => console.error('Error fetching data:', error));
    }
}

// Event listener for window resize
window.addEventListener('resize', function () {
    // Redraw all charts when the window is resized
    createBarChart(labels, dataValues, "percentile");
    createBarChart(labels, grades, "grade");
});