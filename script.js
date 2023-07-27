function calculate() {
    const expression = document.getElementById("expression").value;

    // Remove white spaces from the expression
    const cleanedExpression = expression.replace(/\s/g, '');

    // Prepare the request payload as a JSON object
    const payload = {
        expression: cleanedExpression
    };

    // Send a POST request to the backend server
    fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        if (data.hasOwnProperty('result')) {
            document.getElementById("result").innerText = `Result: ${data.result}`;
        } else if (data.hasOwnProperty('error')) {
            document.getElementById("result").innerText = `Error: ${data.error}`;
        } else {
            document.getElementById("result").innerText = "Error: Invalid response from server";
        }
    })
    .catch(error => {
        // Handle any error that occurred during the request
        document.getElementById("result").innerText = "Error: Unable to connect to the server";
    });
}
