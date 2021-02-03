console.log("Hello Dashboard")

// ------------------  Line Chart ------------------------------------
var lineCtx = document.getElementById('lineChart').getContext('2d');
var lineChart = new Chart (lineCtx, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: "My First Dataset",
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
        }, {
            label: "My Second Dataset",
            backgroundColor: 'rgb(132, 99, 255)',
            borderColor: 'rgb(132, 99, 255)',
            data: [10, 22, 45, 12, 25, 40, 33]
        }]
    },
    options: {
        title : { display : true, position : 'top', text : "Example Line Chart" }
        }
});


// ---------------------- Bar Chart -----------------------------------
var barCtx = document.getElementById('barChart').getContext('2d');
var barChart = new Chart (barCtx, {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: "My First Dataset",
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45],
        }, {
            label: "My Second Dataset",
            backgroundColor: 'rgb(132, 99, 255)',
            borderColor: 'rgb(132, 99, 255)',
            hoverBorderColor: 'rgb(9, 9, 9)',
            hoverBorderWidth : 1,
            data: [-10, 22, 45, -12, 25, 40, 33]
        }]
    },
    options: {
        title : { display : true, position : 'top', text : "Example Bar Chart" }
        }
});

// ---------------------- Radar Chart -----------------------------------
var radarCtx = document.getElementById('radarChart').getContext('2d');
var radarChart = new Chart (radarCtx, {
    type: 'radar',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: "My First Dataset",
            backgroundColor: 'rgba(255, 99, 132, 0.3)',
            borderColor: 'rgba(255, 99, 132, 0.3)',
            data: [0, 10, 5, 2, 20, 30, 45],
        }, {
            label: "My Second Dataset",
            backgroundColor: 'rgba(132, 99, 255, 0.3)',
            borderColor: 'rgba(132, 99, 255, 0.3)',
            data: [-10, 22, 45, -12, 25, 40, 33]
        }]
    },
    options: {
        title : { display : true, position : 'top', text : "Example radar Chart" },
        }
});
// ----------------------- Dougnut / Pie Chart ----------------------------
var pieCtx = document.getElementById('pieChart').getContext('2d');
var pieChart = new Chart (pieCtx, {
    type: 'pie',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: "My First Dataset",
            backgroundColor: [
                '#e60a0a',
                '#3f3dea',
                '#e84ae4',
                '#4ae873',
                '#f7b947',
                '#47f7f7',
                '#ffeb3b',
            ],
            borderColor: 'rgb(50, 50, 50)',
            data: [2, 10, 5, 2, 20, 30, 45],
        },]
    },
    options: {
        title : { display : true, position : 'top', text : "Example Pie Chart" },
        cutoutPercentage : 30,
        }
});

// ----------------------- Polar Area Chart ----------------------------
var polarAreaCtx = document.getElementById('polarAreaChart').getContext('2d');
var polarAreaChart = new Chart (polarAreaCtx, {
    type: 'polarArea',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: "My First Dataset",
            backgroundColor: [
                '#e60a0a',
                '#3f3dea',
                '#e84ae4',
                '#4ae873',
                '#f7b947',
                '#47f7f7',
                '#ffeb3b',
            ],
            borderAlign : 'inner',
            data: [2, 10, 5, 12, 20, 30, 25],
        },]
    },
    options: {
        title : { display : true, position : 'top', text : "Example PolarArea Chart" },
        }
});

// ----------------------- Bubble Chart ----------------------------
var bubbleCtx = document.getElementById('bubbleChart').getContext('2d');
var bubbleChart = new Chart (bubbleCtx, {
    type: 'bubble',
    data: {
        datasets: [{
            label: "My First Dataset",
            backgroundColor: 'rgba(255, 99, 132, 0.3)',
            borderColor: 'rgba(255, 99, 132, 0.3)',
            data: [
                {x: 5, y: 11, r: 10},
                {x: 2, y: 1, r: 9},
                {x: 5.3, y: 8, r: 18},
                {x: 8, y: 11, r: 14},
                {x: 2, y: 10, r: 12},
                {x: 8, y: 12, r: 17},
                ],
        }, {
            label: "My Second Dataset",
            backgroundColor: 'rgba(132, 99, 255, 0.3)',
            borderColor: 'rgba(132, 99, 255, 0.3)',
            data: [
                {x: 1.9, y: 6, r: 19},
                {x: 6, y: 5, r: 8},
                {x: 1.2, y: 3, r: 8},
                {x: 2, y: 5, r: 5},
                {x: 1.5, y: 2, r: 11},
                {x: 2, y: 3, r: 5},
                ],
        }],
    },
    options: {
        title : { display : true, position : 'top', text : "Example Bubble Chart" },
        }
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