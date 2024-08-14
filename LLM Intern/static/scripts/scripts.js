document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    let formData = new FormData(this);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Clear any previous response
        const tableBody = document.querySelector('#responseTable tbody');
        tableBody.innerHTML = ''; // Clear previous rows

        // Assuming `data.response` contains tabular data in the format specified
        if (data.response) {
            // Split the response into lines and process each line
            const lines = data.response.split('\n').filter(line => line.trim() !== '');
            
            lines.forEach(line => {
                // Extract details from the line
                const [detail, value] = line.split(':').map(item => item.trim());
                
                if (detail && value) {
                    // Create a new row
                    const row = document.createElement('tr');
                    const detailCell = document.createElement('td');
                    const valueCell = document.createElement('td');
                    
                    detailCell.textContent = detail;
                    valueCell.textContent = value;
                    
                    row.appendChild(detailCell);
                    row.appendChild(valueCell);
                    
                    tableBody.appendChild(row);
                }
            });
        } else {
            // Handle the case where there is no response
            tableBody.innerHTML = '<tr><td colspan="2">No details found</td></tr>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
