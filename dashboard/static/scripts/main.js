console.log("Hello Dashboard")

//create One State Daily Cases Chart
var lineCtx1sDC = document.getElementById('oneStateDCLineChart').getContext('2d');
var lineChart1sDC = new Chart (lineCtx1sDC, {
                type: 'line',
                data: {},
                options: {
                    title : {
                        display : true,
                        position : 'top',
                        text : "One State Daily Cases" },
                }
            });

// Create Four States Daily Cases Chart
var lineCtx4sDC = document.getElementById('fourStatesDCCanvas').getContext('2d');
var FourStatesDCChart = new Chart (lineCtx4sDC, {
                type: 'line',
                data: {},
                options: {
                    title: {
                        display: true,
                        position: 'bottom',
                        text: '4 States Daily Cases' },
                    scales: {
                        xAxes: [{
                            type: 'time', 
                            time: {
                                unit: 'day',
                                displayFormats: {
                                    'day': 'MMM DD'}},
                        ticks: {source: 'data', maxRotation: 90, autoSkip: true, autoSkipPadding: 5},
                        }]
                    },
                }
            });

function arrayToXY(arr) {
    var newArr = [];
    for (i = 0; i < arr.length; i++) {
        var xy = {};
        xy['x'] = arr[i][0];
        xy['y'] = arr[i][1];
        newArr.push(xy);
    }
    console.log(newArr)
    return newArr;
}

// ------------------  One State Line Chart ------------------------------------
$("#oneStateDC").submit(function(e) {
    e.preventDefault();
    console.log("Got it!  Prevented Default!");
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            console.log(data);
            var newData = {
                labels: data.labels,
                datasets: [{
                    label: data.state_name,
                    borderColor: 'rgb(13, 110, 253)',
                    borderWidth: 1,
                    lineTension: 0.5,
                    pointHoverRadius: 2,
                    pointRadius: 1, 
                    data: data.state_data,
                }]
            };
            
            lineChart1sDC.data = newData;
            lineChart1sDC.update();
        }
    });
});

// ------------------  Line Chart ------------------------------------
$("#fourStatesDC").submit(function(e) {
    e.preventDefault();
    console.log("Got it!  Prevented Default!");
    var form = $(this);
    var url = form.attr('action');
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function(data) {
            console.log(data);
            var newData = { 
                datasets: [{
                    label: data.state_1_name,
                    borderColor: 'rgb(13, 110, 253)',
                    borderWidth: 1,
                    lineTension: 0.5,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_1_data),
                }, {
                    label: data.state_2_name,
                    borderColor: 'rgb(25,135, 84)',
                    borderWidth: 1,
                    lineTension: 0.5,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_2_data),
                }, {
                    label: data.state_3_name,
                    borderColor: 'rgb(220,53, 69)',
                    borderWidth: 1,
                    lineTension: 0.5,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_3_data),
                }, {
                    label: data.state_4_name,
                    borderColor: 'rgb(255,193, 7)',
                    borderWidth: 1,
                    lineTension: 0.5,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_4_data),
                }]
            };

            FourStatesDCChart.data = newData;
            FourStatesDCChart.update();
        }
    });
});


// ----------------------- Scatter Chart ----------------------------
var scatterCtx = document.getElementById('scatterChart').getContext('2d');
var scatterChart = new Chart (scatterCtx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: "My First Dataset",
            backgroundColor: 'rgba(255, 99, 132, 0.3)',
            borderColor: 'rgba(255, 99, 132, 0.3)',
            data: [
                {x: 5, y: 11},
                {x: 2, y: 1},
                {x: 5.3, y: 8},
                {x: 8, y: 11},
                {x: 2, y: 10},
                {x: 8, y: 12},
                ],
        }, {
            label: "My Second Dataset",
            backgroundColor: 'rgba(132, 99, 255, 0.3)',
            borderColor: 'rgba(132, 99, 255, 0.3)',
            data: [
                {x: 1.9, y: 6},
                {x: 6, y: 5},
                {x: 5, y: 3},
                {x: 2, y: 5},
                {x: 1.5, y: 2},
                {x: 4, y: 3.5},
                ],
        }],
    },
    options: {
        title : { display : true, position : 'top', text : "Example Scatter Chart" },
        }
});

