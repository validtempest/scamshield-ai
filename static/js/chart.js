document.addEventListener(
    'DOMContentLoaded',
    () => {

        const ctx =
            document.getElementById(
                'scamChart'
            );

        if (!ctx) return;

        const chartData =
            JSON.parse(
                document
                    .getElementById(
                        'chart-data'
                    )
                    .textContent
            );

        const {
            scamCount,
            safeCount
        } = chartData;

        new Chart(ctx, {

            type: 'doughnut',

            data: {

                labels: [
                    'Ancaman Scam',
                    'Tanda Aman'
                ],

                datasets: [{

                    data: [
                        scamCount,
                        safeCount
                    ],

                    backgroundColor: [
                        '#f43f5e', /* rose */
                        '#10b981'  /* emerald */
                    ],

                    borderColor: '#0B1120', /* Matches base navy background */
                    borderWidth: 3,
                    hoverOffset: 4
                }]
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#cbd5e1', /* slate-300 matching text */
                            font: {
                                family: 'Inter',
                                size: 12,
                                weight: '500'
                            },
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        titleFont: {
                            family: 'Inter',
                            size: 13,
                            weight: 'bold'
                        },
                        bodyFont: {
                            family: 'Inter',
                            size: 12
                        },
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: true,
                        boxWidth: 8,
                        boxHeight: 8,
                        boxPadding: 4,
                        cornerRadius: 8
                    }
                },
                cutout: '70%' /* Creates a highly modern, sleek thin doughnut */
            }
        });
    }
);