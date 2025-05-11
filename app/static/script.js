const ctx = document.getElementById('myChart').getContext('2d');
        let chart;

        function updateChart(indicator) {
            fetch(`/chart-data?indicator=${encodeURIComponent(indicator)}`)
                .then(res => res.json())
                .then(data => {
                    const labels = data.map(entry => entry.date);
                    const values = data.map(entry => entry.value);

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
                                    beginAtZero: false
                                }
                            }
                        }
                    });
                });
        }

        // Populate dropdown with indicators
        fetch('/indicators')
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

document.getElementById('customButton').addEventListener('click', () => {
  const fileInput = document.getElementById('fileInput');
  fileInput.click();

  fileInput.onchange = () => {
    if (fileInput.files.length > 0) {
      document.getElementById('uploadForm').submit();  // Submit the form here
    }
  };
});