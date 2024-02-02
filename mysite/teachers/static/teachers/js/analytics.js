const btnDiv = document.getElementById('search-students');
const closeBtn = document.getElementById('close')
const courseDiv = document.getElementById('coursediv');
const content = document.getElementById('content')

// Add a click event listener to the trigger div
btnDiv.addEventListener('click', function () {
    // Toggle the display style of the target div
    content.style.display = 'none';
    courseDiv.style.display = 'flex';
});

closeBtn.addEventListener('click', function () {
    // Toggle the display style of the target div
    content.style.display = 'flex';
    courseDiv.style.display = 'none';
});

const divs = document.querySelectorAll('.grades');

// Add a click event listener to each div
divs.forEach(function(div) {
    div.addEventListener('click', function() {
        // Your event handling code here
        studentId = div.getAttribute('data-class-studentId');
        window.location.href = `/teachers/student_report/${studentId}/`;
    });
});

var chartDataArray = [];

function createPieChart(courseId, labels, data) {
    var ctx = document.getElementById('chart-' + courseId).getContext('2d');



    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
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
    });
    return myPieChart;
}

fetch('/teachers/analytics/', {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
    }
})
.then(response => response.json())
.then(data => {
    data.forEach(grade => {
        var courseId = grade.course_id;
        var gradeCheck = grade.grade_check;
        var labels = Object.keys(grade.grade_counts);
        var dataValues = Object.values(grade.grade_counts);
        console.log(dataValues)
        if(gradeCheck > 0){
            chartDataArray.push({
                courseId: courseId,
                labels: labels,
                dataValues: dataValues
            });
            createPieChart(courseId, labels, dataValues);
        }
    });
})
.catch(error => console.error('Error fetching data:', error));

// Event listener for window resize
window.addEventListener('resize', function () {
    // Redraw all charts when the window is resized
    chartDataArray.forEach(chartData => {
        createPieChart(chartData.courseId, chartData.labels, chartData.dataValues);
    });
});