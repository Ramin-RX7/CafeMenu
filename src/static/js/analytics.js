function fetchDataFromAPI() {
    return fetch('/dashboard/analytics-api/')
        .then(response => response.json())
        .catch(error => {
            console.error('Error fetching sales data:', error);
            throw error; // Propagate the error
        });
}



// set up the config for comparative charts
function _getComparativeChartConfig(labels, oldData, newData){
    return {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'This',
                    data: newData,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Previous',
                    data: oldData,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    hidden: true
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
}

// set up the config for relative charts
function _getRelativeChartConfig(labels, data){
    return {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Data',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
}

// Get a list of labels based on array length
function _getDurationLabels(array){
    switch (array.length) {
        case 24:
            return Array.from({ length: 24 }, (_, index) => (index + 1).toString());
        case 31:
            return Array.from({ length: 31 }, (_, index) => (index).toString());
        case 7:
            return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        case 12:
            return ["Jan", "Feb", "Mar", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    }
}


function getChartConfig(fulltype, full_data) {
    let [main_type,sub_type] = fulltype.split(":");
    let chartConfig;
    if (main_type=="Comparative"){
        let oldData = full_data[main_type][sub_type][0];
        let newData = full_data[main_type][sub_type][1];
        let labels  = _getDurationLabels(newData)
        chartConfig = _getComparativeChartConfig(labels, oldData, newData)
    } else {
        let data = full_data[main_type][sub_type]
        let labels = _getDurationLabels(data)
        chartConfig = _getRelativeChartConfig(labels, data)
    }
    return chartConfig
}












function createChartWithData(oldData, newData) {
    const ctx = document.getElementById('salesChart').getContext('2d');
    const labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
    const chartConfig = getChartConfig(labels, oldData, newData);

    // Create the chart
    const salesChart = new Chart(ctx, chartConfig);

    // Toggle button functionality
    const toggleButton = document.getElementById('toggleButton');
    toggleButton.addEventListener('click', () => {
        // Toggle the hidden property of the last week's dataset
        salesChart.data.datasets[1].hidden = !salesChart.data.datasets[1].hidden;
        salesChart.update(); // Update the chart to reflect changes
    });
}


fetchDataFromAPI().then(data => {
    const thisWeekData = data.sales;
    const lastWeekData = [5, 8, 6, 2, 4];
    createChartWithData(thisWeekData, lastWeekData);

});