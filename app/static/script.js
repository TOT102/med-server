const ctx = document.getElementById('myChart').getContext('2d');
        let chart;

        async function updateChart(indicator) {
            const chartData = await fetch(`chart-data?indicator=${encodeURIComponent(indicator)}`).then(res => res.json());
            const marginValues = await fetch(`get-margin-values?indicator=${encodeURIComponent(indicator)}`).then(res => res.json());

            const labels = chartData.map(entry => entry.date);
            const values = chartData.map(entry => entry.value);

            const maxYValue = Math.max(...values);
            //const buffer = (maxYValue * 0.2); // 20% buffer above data range
            const chartMaxY = maxYValue*1.5;

            if (chart) chart.destroy();

            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: indicator,
                        data: values,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 2,
                        fill: false,
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: false,
                            suggestedMax: chartMaxY
                        }
                    },
                    plugins: {
                        annotation: {
                            annotations: {
                                unsafeLow: {
                                    type: 'box',
                                    yMin: 0,
                                    yMax: marginValues.min,
                                    xMin: 0,
                                    xMax: labels.length - 1,
                                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                                    borderWidth: 0,
                                    /*label: {
                                        enabled: true,
                                        content: 'Below safe range',
                                        position: 'start'
                                    }*/
                                },
                                unsafeHigh: {
                                    type: 'box',
                                    yMin: marginValues.max,
                                    yMax: chartMaxY*1.2,
                                    xMin: 0,
                                    xMax: labels.length - 1,
                                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                                    borderWidth: 0,
                                    /*label: {
                                        enabled: true,
                                        content: 'Above safe range',
                                        position: 'end'
                                    }*/
                                }
                            }
                        }
                    }
                },
                plugins: [Chart.registry.getPlugin('annotation')]
            });
        }


        // Populate dropdown with indicators
        fetch('indicators')
            .then(res => res.json())
            .then(indicators => {
                const select = document.getElementById('indicatorSelect');
                select.innerHTML = ''; // Clear loading text

                indicators.forEach(indicator => {
                    const option = document.createElement('option');
                    option.value = indicator;
                    option.textContent = indicator;
                    select.appendChild(option);
                });

                select.addEventListener('change', () => {
                    updateChart(select.value);
                    fetchMaxValue(select.value);
                    fetchAvgValue(select.value);
                    fetchMinValue(select.value);
                });
            });

    //         async function fetchIndicatorValue() {
    //   try {
    //     const response = await fetch('http://127.0.0.1:5000/get-margin-values?indicator=P-LCR');
    //     const data = await response.json();
    //     document.getElementById('value-box').innerText = data.value; // Adjust depending on your JSON
    //   } catch (error) {
    //     document.getElementById('value-box').innerText = 'Error loading data';
    //     console.error(error);
    //   }
    // }

/*document.getElementById('customButton').addEventListener('click', () => {
  const fileInput = document.getElementById('fileInput');
  fileInput.click();

  fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
      document.getElementById('uploadForm').submit();  // Submit the form here
    }
  };
});

document.getElementById('customButton').addEventListener('click', function () {
  document.getElementById('fileInput').click();
});*/

const fileInput = document.getElementById('fileInput');
const customButton = document.getElementById('customButton');
const uploadForm = document.getElementById('uploadForm');

customButton.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  if (fileInput.files.length > 0) {
    uploadForm.submit();

    const popup = document.getElementById('uploadSuccessPopup');
    popup.classList.remove('hidden');
    popup.classList.add('show');

    setTimeout(() => {
      popup.classList.remove('show');
      popup.classList.add('hidden');
    }, 10000);
  }
});

function fetchMaxValue(indicator) {
    fetch(`get-max?indicator=${encodeURIComponent(indicator)}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('maxValue').textContent = data;  
        })
        .catch(err => {
            console.error('Failed to fetch max value:', err);
            document.getElementById('maxValue').textContent = 'Error';
        });
}

function fetchMinValue(indicator) {
    fetch(`get-min?indicator=${encodeURIComponent(indicator)}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById('minValue').textContent = data;  
        })
        .catch(err => {
            console.error('Failed to fetch min value:', err);
            document.getElementById('minValue').textContent = 'Error';
        });
}

function fetchAvgValue(indicator) {
    fetch(`get-avg?indicator=${encodeURIComponent(indicator)}`)
        .then(res => res.json())
        .then(data => {
            const roundedAvg = Number(data).toFixed(2);
            document.getElementById('avgValue').textContent = roundedAvg;  
        })
        .catch(err => {
            console.error('Failed to fetch avg value:', err);
            document.getElementById('avgValue').textContent = 'Error';
        });
}

async function fetchMarginValues(indicator) {
    const response = await fetch(`get-margin-values?indicator=${encodeURIComponent(indicator)}`);
    const data = await response.json();
    return data;
}