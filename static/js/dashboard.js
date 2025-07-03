/**
 * Dashboard de Administración - Plataforma Médica Universitaria
 * Manejo de gráficos estadísticos y visualizaciones
 */

const DashboardApp = {
    // Configuración de colores institucionales
    colores: {
        primario: '#1e3a8a',
        secundario: '#6b7280',
        exito: '#059669',
        advertencia: '#d97706',
        peligro: '#dc2626',
        info: '#0284c7',
        fondo: '#f8fafc'
    },

    // Configuración de Chart.js
    configuracionBase: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true,
                    padding: 20,
                    font: {
                        family: 'Roboto, sans-serif',
                        size: 12
                    }
                }
            }
        }
    },

    /**
     * Inicializa el dashboard
     */
    init: function() {
        console.log('Inicializando Dashboard Administrativo...');
        this.cargarGraficos();
        this.configurarEventos();
        this.actualizarEstadisticas();
    },

    /**
     * Carga todos los gráficos del dashboard
     */
    cargarGraficos: function() {
        this.cargarGraficoCitasPorTipo();
        this.cargarGraficoConsultasPorCarrera();
        this.cargarGraficoTendenciaMensual();
        this.cargarGraficoNivelesRiesgo();
    },

    /**
     * Carga el gráfico de citas por tipo
     */
    cargarGraficoCitasPorTipo: function() {
        const ctx = document.getElementById('citasTipoChart');
        if (!ctx) return;

        fetch('/reportes/api/estadisticas-citas')
            .then(response => response.json())
            .then(data => {
                const labels = Object.keys(data);
                const valores = Object.values(data);
                
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: labels.map(label => this.traducirTipoCita(label)),
                        datasets: [{
                            data: valores,
                            backgroundColor: [
                                this.colores.primario,
                                this.colores.info,
                                this.colores.peligro
                            ],
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        ...this.configuracionBase,
                        plugins: {
                            ...this.configuracionBase.plugins,
                            title: {
                                display: true,
                                text: 'Distribución de Citas por Tipo',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error al cargar estadísticas de citas:', error);
                this.mostrarErrorGrafico('citasTipoChart', 'Error al cargar datos de citas');
            });
    },

    /**
     * Carga el gráfico de consultas por carrera
     */
    cargarGraficoConsultasPorCarrera: function() {
        const ctx = document.getElementById('consultasCarreraChart');
        if (!ctx) return;

        fetch('/reportes/api/estadisticas-carreras')
            .then(response => response.json())
            .then(data => {
                const labels = Object.keys(data);
                const valores = Object.values(data);
                
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Consultas',
                            data: valores,
                            backgroundColor: this.colores.exito,
                            borderColor: this.colores.exito,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        ...this.configuracionBase,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        },
                        plugins: {
                            ...this.configuracionBase.plugins,
                            title: {
                                display: true,
                                text: 'Consultas por Carrera',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error al cargar estadísticas de carreras:', error);
                this.mostrarErrorGrafico('consultasCarreraChart', 'Error al cargar datos de carreras');
            });
    },

    /**
     * Carga el gráfico de tendencia mensual
     */
    cargarGraficoTendenciaMensual: function() {
        const ctx = document.getElementById('tendenciaMensualChart');
        if (!ctx) return;

        fetch('/reportes/api/tendencia-mensual')
            .then(response => response.json())
            .then(data => {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.meses,
                        datasets: [{
                            label: 'Citas por Mes',
                            data: data.totales,
                            borderColor: this.colores.primario,
                            backgroundColor: this.colores.primario + '20',
                            tension: 0.4,
                            fill: true
                        }]
                    },
                    options: {
                        ...this.configuracionBase,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    stepSize: 1
                                }
                            }
                        },
                        plugins: {
                            ...this.configuracionBase.plugins,
                            title: {
                                display: true,
                                text: 'Tendencia Mensual de Citas',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error al cargar tendencia mensual:', error);
                this.mostrarErrorGrafico('tendenciaMensualChart', 'Error al cargar tendencia mensual');
            });
    },

    /**
     * Carga el gráfico de niveles de riesgo
     */
    cargarGraficoNivelesRiesgo: function() {
        const ctx = document.getElementById('nivelesRiesgoChart');
        if (!ctx) return;

        fetch('/reportes/api/niveles-riesgo')
            .then(response => response.json())
            .then(data => {
                const labels = Object.keys(data);
                const valores = Object.values(data);
                
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels.map(label => this.traducirNivelRiesgo(label)),
                        datasets: [{
                            data: valores,
                            backgroundColor: [
                                this.colores.exito,    // Bajo
                                this.colores.advertencia, // Medio
                                this.colores.peligro,  // Alto
                                '#1f2937'              // Crítico
                            ],
                            borderWidth: 2,
                            borderColor: '#ffffff'
                        }]
                    },
                    options: {
                        ...this.configuracionBase,
                        plugins: {
                            ...this.configuracionBase.plugins,
                            title: {
                                display: true,
                                text: 'Distribución de Niveles de Riesgo',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error al cargar niveles de riesgo:', error);
                this.mostrarErrorGrafico('nivelesRiesgoChart', 'Error al cargar niveles de riesgo');
            });
    },

    /**
     * Configura eventos del dashboard
     */
    configurarEventos: function() {
        // Evento para actualizar estadísticas
        const btnActualizar = document.querySelector('.btn-actualizar');
        if (btnActualizar) {
            btnActualizar.addEventListener('click', () => {
                this.actualizarEstadisticas();
            });
        }

        // Animaciones de entrada para las tarjetas
        const tarjetas = document.querySelectorAll('.stat-card');
        tarjetas.forEach((tarjeta, index) => {
            setTimeout(() => {
                tarjeta.classList.add('fade-in');
            }, index * 100);
        });
    },

    /**
     * Actualiza las estadísticas generales
     */
    actualizarEstadisticas: function() {
        console.log('Actualizando estadísticas...');
        
        // Mostrar indicador de carga
        const indicadores = document.querySelectorAll('.stat-card .card-body h3');
        indicadores.forEach(indicador => {
            indicador.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        });

        // Simular actualización (en producción, esto haría una llamada AJAX)
        setTimeout(() => {
            window.location.reload();
        }, 1500);
    },

    /**
     * Muestra un mensaje de error en lugar del gráfico
     */
    mostrarErrorGrafico: function(canvasId, mensaje) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        const contenedor = canvas.parentElement;
        contenedor.innerHTML = `
            <div class="d-flex flex-column align-items-center justify-content-center h-100 text-muted">
                <i class="fas fa-exclamation-triangle fa-3x mb-3"></i>
                <p class="text-center">${mensaje}</p>
                <button class="btn btn-sm btn-outline-primary" onclick="location.reload()">
                    <i class="fas fa-sync-alt me-2"></i>Reintentar
                </button>
            </div>
        `;
    },

    /**
     * Traduce los tipos de cita del inglés al español
     */
    traducirTipoCita: function(tipo) {
        const traducciones = {
            'TipoCita.MEDICINA': 'Medicina',
            'TipoCita.PSICOLOGIA': 'Psicología',
            'TipoCita.EMERGENCIA': 'Emergencia',
            'MEDICINA': 'Medicina',
            'PSICOLOGIA': 'Psicología',
            'EMERGENCIA': 'Emergencia'
        };
        return traducciones[tipo] || tipo;
    },

    /**
     * Traduce los niveles de riesgo del inglés al español
     */
    traducirNivelRiesgo: function(nivel) {
        const traducciones = {
            'NivelRiesgo.BAJO': 'Bajo',
            'NivelRiesgo.MEDIO': 'Medio',
            'NivelRiesgo.ALTO': 'Alto',
            'NivelRiesgo.CRITICO': 'Crítico',
            'BAJO': 'Bajo',
            'MEDIO': 'Medio',
            'ALTO': 'Alto',
            'CRITICO': 'Crítico'
        };
        return traducciones[nivel] || nivel;
    },

    /**
     * Formatea números para mostrar en las estadísticas
     */
    formatearNumero: function(numero) {
        return new Intl.NumberFormat('es-ES').format(numero);
    },

    /**
     * Formatea fechas para mostrar en español
     */
    formatearFecha: function(fecha) {
        return new Intl.DateTimeFormat('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(fecha));
    }
};

// Utilidades adicionales para el dashboard
const Utils = {
    /**
     * Muestra notificaciones toast
     */
    mostrarNotificacion: function(mensaje, tipo = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${tipo} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${mensaje}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remover el elemento después de que se oculte
        toast.addEventListener('hidden.bs.toast', () => {
            document.body.removeChild(toast);
        });
    },

    /**
     * Confirma acciones importantes
     */
    confirmarAccion: function(mensaje, callback) {
        if (confirm(mensaje)) {
            callback();
        }
    },

    /**
     * Maneja errores de red
     */
    manejarErrorRed: function(error) {
        console.error('Error de red:', error);
        this.mostrarNotificacion('Error de conexión. Verifica tu conexión a internet.', 'danger');
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Configurar Chart.js por defecto
    Chart.defaults.font.family = 'Roboto, sans-serif';
    Chart.defaults.color = '#6b7280';
    Chart.defaults.borderColor = '#e5e7eb';
    
    // Configurar tooltips personalizados
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(31, 41, 55, 0.9)';
    Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
    Chart.defaults.plugins.tooltip.bodyColor = '#ffffff';
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    
    console.log('Dashboard JavaScript cargado correctamente');
});
