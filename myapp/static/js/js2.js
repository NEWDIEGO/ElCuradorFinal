document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gráficos con Chart.js o similar
    if (document.getElementById('citasPorEspecialidadChart')) {
        var ctx = document.getElementById('citasPorEspecialidadChart').getContext('2d');
        var citasPorEspecialidadChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: JSON.parse(document.getElementById('citasPorEspecialidadLabels').textContent),
                datasets: [{
                    label: 'Citas',
                    data: JSON.parse(document.getElementById('citasPorEspecialidadData').textContent),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    if (document.getElementById('atencionPorEstadoChart')) {
        var ctx2 = document.getElementById('atencionPorEstadoChart').getContext('2d');
        var atencionPorEstadoChart = new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: JSON.parse(document.getElementById('atencionPorEstadoLabels').textContent),
                datasets: [{
                    label: 'Atención por Estado',
                    data: JSON.parse(document.getElementById('atencionPorEstadoData').textContent),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                var label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += context.parsed + ' citas';
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }
});
