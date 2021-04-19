
// Create Four States Daily Cases Chart
var lineCtxUSTotals = document.getElementById('USTotalsCanvas').getContext('2d');
var USTotalsChart = new Chart (lineCtxUSTotals, {
                type: 'line',
                data: {},
                options: {
                    title: {
                        display: true,
                        text: 'U.S. Cumulative Covid-19 Cases',
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
$("#USTotalsForm").submit(function(e) {
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
                    label: data.data_name,
                    borderColor: 'rgb(13, 110, 253)',
                    borderWidth: 1,
                    lineTension: 0,
                    pointHoverRadius: 2,
                    pointRadius: 1,
                    data: arrayToXY(data.dataset),
                }]
            };

            USTotalsChart.data = newData;
            USTotalsChart.options.title.text = data.title;
            USTotalsChart.update();
        }
    });
});

function showDiv(divId, element, value) {
    document.getElementById(divId).style.display = element.value == value ? 'block' : 'none';
}