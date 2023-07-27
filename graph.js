let myChart = null;

function drawGraph(data) {
    let canvas = document.getElementById('graphCanvas');
    let ctx = canvas.getContext('2d');
    
    // Set the dimensions of the canvas to match its CSS dimensions
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    // If a chart already exists, destroy it
    if (myChart) {
        myChart.destroy();
    }

    // Create a new chart
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(pair => pair[0]),
            datasets: [{
                label: 'Graph of function',
                data: data.map(pair => pair[1]),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        }
    });
}

function graph() {
    console.log("Graph function called");
    const funcExpression = document.getElementById("expression").value;
    const rangeStart = document.getElementById("lowerBound").value;
    const rangeEnd = document.getElementById("upperBound").value;
    // Assuming you've provided the steps input field with an id of "steps"
    const steps = document.getElementById("steps").value;

    const payload = {
        funcExpression: funcExpression,
        rangeStart: parseFloat(rangeStart),
        rangeEnd: parseFloat(rangeEnd),
        steps: parseInt(steps),
    };

    fetch('http://localhost:5000/graph', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Data received from server: ", data);
        drawGraph(data);
    })
    .catch(error => {
        // Handle any error that occurred during the request
        console.log("Error fetching data from server: ", error);
    });
}
