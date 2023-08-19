function fetchDataFromAPI() {
    return fetch('/dashboard/analytics-api/')
        .then(response => response.json())
        .catch(error => {
            console.error('Error fetching sales data:', error);
            throw error; // Propagate the error
        });
}


function flattenNestedObject(obj, prefix = '', depth = 0, maxDepth = 3) {
    const result = {};
    for (const key in obj) {
        const value = obj[key];
        if (depth < maxDepth && typeof value === 'object' && !Array.isArray(value)) {
            const nestedPrefix = prefix ? `${prefix}:${key}` : key;
            const nestedFlattened = flattenNestedObject(value, nestedPrefix, depth + 1, maxDepth);
            Object.assign(result, nestedFlattened);
        } else {
            result[prefix ? `${prefix}:${key}` : key] = value;
        }
    }
    return result;
}


// set up the config for comparative charts
function _getChartConfig(labels, data, other_data=null){
    let config = {
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'This',
                    data: data,
                    backgroundColor: 'rgba(190,140,75, 0.6)',
                    borderColor: "#bc8c4c",
                    borderWidth: 5
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

    if (other_data === null){
        config.type = "bar"
    } else {
        config.type = "line"
        config.data.datasets.push({
            label: 'Previous',
            data: other_data,
            backgroundColor: 'rgba(190,190,190, 0.6)',
            borderColor: '#bdbebf',
            borderWidth: 5,
            hidden: true
        })
    }
    return config
}



// Get a list of labels for chart based on the name or dictionary keys
function _getDurationLabels(duration, fulltype, data){
    let type = fulltype.split(":")[1]
    if (!Array.isArray(data)){
        if (!Array.isArray(data.new)){
            try {
                return Object.keys(data.new)
            } catch (error) {
            }
        }
        data = data.new;
    }
    switch (duration) {
        case "day":
            let hours = Array.from({ length: 24 }, (_, index) => (index).toString());
            if (type === "relative"){
                return hours.reverse()
            }
            return hours
        case "month":
            let days = Array.from({ length: 30 }, (_, index) => (index+1).toString());
            if (type === "relative"){
                return days.reverse()
            }
            return days;
        case "week":
            const weekArray = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
            if (type === "relative"){
                return [7,6,5,4,3,2,1];
            }
            return weekArray
        case "year":
            const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            if (type === "relative"){
                return [12,11,10,9,8,7,6,5,4,3,2,1];
            }
            return months
    }
    return Object.keys(data)
}

// Get values of the chart (y axis) and return them in an array of arrays.
function _getValues(duration_data){
    if (!Array.isArray(duration_data)){
        if (!Array.isArray(duration_data.new)){
            return [duration_data.new, duration_data.old]
        } else {
            return [Object.values(duration_data.new), Object.values(duration_data.old)]
        }
    } else {
        return [duration_data,null]
    }
}



function getChartConfig(duration, fulltype, data) {
    let labels =  _getDurationLabels(duration, fulltype, data)
    let [newData,oldData] =  _getValues(data)
    let chartConfig = _getChartConfig(labels, newData, oldData)
    return chartConfig
}

function createChartWithData(duration, fulltype, data) {
    let ctx;
    try {
        ctx = document.getElementById(fulltype).getContext('2d');
    } catch (error) {
        return null
    }
    const chartConfig = getChartConfig(duration, fulltype, data);
    const salesChart = new Chart(ctx, chartConfig);
}



fetchDataFromAPI().then(data => {
    const flattenedData = flattenNestedObject(data, '', 0, 2);
    for (const fulltype in flattenedData) {
        console.log(fulltype);
        const data = flattenedData[fulltype];
        duration_name = fulltype.split(":").pop();
        createChartWithData(duration_name, fulltype, data);
    }
});






document.querySelectorAll('.download-btn').forEach(function(button) {
    button.addEventListener('click', function() {
        let chartId = button.getAttribute('data-chart-id');
        let canvas = document.getElementById(chartId);
        downloadChartAsImage(canvas, chartId);
    });
});

function downloadChartAsImage(canvas, chartId) {
    console.log("here");
    let imageBase64 = canvas.toDataURL('image/png');
    let currentDate = new Date();
    let formattedDate = currentDate.toISOString().split('T')[0]; // YYYY-MM-DD format
    let formattedTime = currentDate.toLocaleTimeString().replace(/:/g, '-'); // HH-MM-SS format
    let filename = chartId.replace(":", "-") + '-' + formattedDate + '-' + formattedTime + '.png';
    let link = document.createElement('a');
    link.href = imageBase64;
    link.download = filename;
    link.click();
}