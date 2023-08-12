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
    config = {
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'This',
                    data: data,
                    backgroundColor: 'rgba(190,140,75, 0.6)',
                    borderColor: "#bc8c4c",
                    borderWidth: 5
                },
                {
                    label: 'Previous',
                    data: other_data,
                    backgroundColor: 'rgba(190,190,190, 0.6)',
                    borderColor: '#bdbebf',
                    borderWidth: 5,
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
    if (other_data == null){
        config.type = "bar"
    } else {
        config.type = "line"
    }
    return config
}

// set up the config for relative charts


// Get a list of labels for chart based on the name or dictionary keys
function _getDurationLabels(duration, data){
    if (typeof data === "object"){
        if (typeof data.old == "object"){
            return Object.keys(data.old)
        }
    }
    switch (duration) {
        case "day":
            return Array.from({ length: 24 }, (_, index) => (index + 1).toString());
        case "month":
            return Array.from({ length: 31 }, (_, index) => (index).toString());
        case "week":
            return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        case "year":
            return ["Jan", "Feb", "Mar", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    }
    return Object.keys(data)
}

function _getValues(duration_data){
    if (Object.prototype.toString.call(duration_data) === "[object Object]"){
        if (typeof duration_data.old === "object"){
            return [Object.values(duration_data.old), Object.values(duration_data.new)]
        } else {
            return [duration_data.old, duration_data.new]
        }
    } else {
        return [duration_data,[]]
    }
}



// Get the chart config from the namespace and DATA
function getChartConfig(fulltype, full_data) {
    let [query,type,duration] = fulltype.split(":");
    let chartConfig;
    let duration_data = full_data[query][type][duration]
    let labels =  _getDurationLabels(duration,duration_data)
    let [oldData,newData]  =  _getValues(duration_data)
    chartConfig = _getComparativeChartConfig(labels, oldData, newData)
    // console.log(old);

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
    // createChartWithData("sales:comparative:week", data);
    createChartWithData("sales:relative:week", data);

});