// A set of default options to ensure a consistent look and feel for all charts.
const defaultChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
        mode: 'index',
        intersect: false,
    },
    plugins: {
        legend: {
            position: 'top',
        },
        tooltip: {
            boxPadding: 4,
            titleFont: {
                weight: 'bold',
            },
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                font: {
                    size: 11,
                }
            }
        },
        y: {
            grid: {
                color: '#e9ecef',
                borderDash: [2, 4],
            },
            beginAtZero: true,
            ticks: {
                font: {
                    size: 11,
                }
            }
        }
    }
};

console.log("GridSight JS initialised.");
