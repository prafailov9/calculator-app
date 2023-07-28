let myChart = null;

function showLoading() {
    document.getElementById("spinner").style.display = "block";
    document.getElementById("overlay").style.display = "block"; // Show the overlay
}

function hideLoading() {
    document.getElementById("spinner").style.display = "none";
    document.getElementById("overlay").style.display = "none"; // Hide the overlay
}

function showOverlay() {
    let overlay = document.getElementById("overlay");
    overlay.style.display = "block";
    setTimeout(() => overlay.style.opacity = "0.5", 10);  // Transition to semi-transparent
}

function hideOverlay() {
    let overlay = document.getElementById("overlay");
    overlay.style.opacity = "0";  // Transition to fully transparent
    // Wait for the transition to finish before hiding the overlay
    setTimeout(() => overlay.style.display = "none", 500);
}

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
    hideLoading(); // Hide the spinner and overlay after the chart has been drawn
    hideOverlay();
}

function graph() {
    console.log("Graph function called");
    const funcExpression = document.getElementById("expression").value;
    const rangeStart = document.getElementById("lowerBound").value;
    const rangeEnd = document.getElementById("upperBound").value;
    const steps = document.getElementById("steps").value;

    const payload = {
        funcExpression: funcExpression,
        rangeStart: parseFloat(rangeStart),
        rangeEnd: parseFloat(rangeEnd),
        steps: parseInt(steps),
    };

    // Display the spinner
    document.getElementById("spinner").style.display = "block";

    const start = Date.now();

    fetch('http://127.0.0.1:5000/graph', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        // Hide the spinner and overlay if there was an error
        if (!response.ok) {
            hideLoading();
            hideOverlay();
        }
        return response.json();
    })
    .then(data => {
        console.log("Data received from server: ", data);
        drawGraph(data);
        // Hide the spinner
        document.getElementById("spinner").style.display = "none";
    })
    .catch(error => {
        // Handle any error that occurred during the request
        console.log("Error fetching data from server: ", error);
        
        hideLoading();
        hideOverlay();
    });
    showLoading(); // Show the spinner and overlay before making the fetch request
    showOverlay();
}
