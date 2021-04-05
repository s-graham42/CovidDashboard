console.log("Hello Dashboard")



// Create Four States Daily Cases Chart
var lineCtxSVOT = document.getElementById('singleVariableOTCanvas').getContext('2d');
var singleVariableOTChart = new Chart (lineCtxSVOT, {
                type: 'line',
                data: {},
                options: {
                    title: {
                        display: true,
                        text: 'Daily Covid-19 Cases',
                    },
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


// ------------------  Line Chart ------------------------------------
$("#singleVariableOTForm").submit(function(e) {
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
                    lineTension: 0,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_1_data),
                }, {
                    label: data.state_2_name,
                    borderColor: 'rgb(25,135, 84)',
                    borderWidth: 1,
                    lineTension: 0,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_2_data),
                }, {
                    label: data.state_3_name,
                    borderColor: 'rgb(220,53, 69)',
                    borderWidth: 1,
                    lineTension: 0,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_3_data),
                }, {
                    label: data.state_4_name,
                    borderColor: 'rgb(255,193, 7)',
                    borderWidth: 1,
                    lineTension: 0,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.state_4_data),
                }]
            };

            singleVariableOTChart.data = newData;
            singleVariableOTChart.options.title.text = data.title;
            singleVariableOTChart.update();
        }
    });
});

