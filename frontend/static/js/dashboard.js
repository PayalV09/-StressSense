if (stressData && stressData.length > 0) {
    const dates = stressData.map(item =>
        new Date(item.timestamp).toLocaleString('en-IN', {
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        })
    );

    const levels = stressData.map(item => parseFloat(item.stress_level) || 0);

    const canvas = document.getElementById('stressTrendChart');
    const ctx = canvas.getContext('2d');

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(255, 99, 132, 0.4)');
    gradient.addColorStop(1, 'rgba(255, 99, 132, 0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Stress Level',
                data: levels,
                backgroundColor: gradient,
                borderColor: '#ff5c8d',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#ff5c8d',
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1200,
                easing: 'easeOutCubic'
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Your Stress Trends Over Time',
                    color: '#ffffff',
                    font: {
                        size: 20,
                        weight: 'bold',
                        family: "'Segoe UI', sans-serif"
                    }
                },
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                },
                tooltip: {
                    backgroundColor: '#002c3e',
                    titleColor: '#ffffff',
                    bodyColor: '#fdfcdc',
                    borderColor: '#ff5c8d',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    min: 0,
                    max: 6,
                    title: {
                        display: true,
                        text: 'Stress Level (0 to 6)',
                        color: '#ffffff'
                    },
                    ticks: {
                        color: '#ffffff'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Submission Timestamp',
                        color: '#ffffff'
                    },
                    ticks: {
                        color: '#ffffff',
                        autoSkip: true,
                        maxRotation: 45,
                        minRotation: 25
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                }
            }
        }
    });
}
