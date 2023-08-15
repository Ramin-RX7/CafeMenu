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
function _getComparativeChartConfig(labels, data, other_data=null){
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
function _getDurationLabels(duration, data){
    // console.log(data);
    if (!Array.isArray(data)){
        if (!Array.isArray(data.new)){
            return Object.keys(data.new)
        }
        data = data.old;
    }
    switch (duration) {
        case "day":
            return Array.from({ length: 24 }, (_, index) => (index).toString());
            case "month":
                return Array.from({ length: 31 }, (_, index) => (index).toString());
        case "week":
            return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
        case "year":
            return ["Jan", "Feb", "Mar", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    }
    return Object.keys(data)
}

// Get values of the chart (y axis) and return them in an array of arrays.
function _getValues(duration_data){
    if (!Array.isArray(duration_data)){
        if (!Array.isArray(duration_data.old)){
            return [duration_data.old, duration_data.new]
        } else {
            return [Object.values(duration_data.old), Object.values(duration_data.new)]
        }
    } else {
        return [duration_data,null]
    }
}



function getChartConfig(duration, data) {
    let labels =  _getDurationLabels(duration,data)
    let [newData,oldData] =  _getValues(data)
    let chartConfig = _getComparativeChartConfig(labels, newData, oldData)
    return chartConfig
}

function createChartWithData(duration, fulltype, data) {
    let ctx;
    try {
        ctx = document.getElementById(fulltype).getContext('2d');
    } catch (error) {
        return null
    }
    const chartConfig = getChartConfig(duration, data);
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
