<template>
    <div class="canvasContainer">
        <Legend :legend-values="legendValues" />
        <canvas ref="chartCanvas"></canvas>
    </div>
</template>

<script>
import Chart from 'chart.js/auto';
import Legend from './Legend.vue';

export default {
    components: {
        Legend
    },
    props: {
        chartData: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            chart: null,
            legendValues: [],
            options: {
                plugins: {
                    legend: {
                        display: false
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: "#b6baca",
                        },
                        grid: {
                            drawTicks: false,
                            borderDash: [5, 5],
                        },
                    },
                    x: {
                        ticks: {
                            color: "#b6baca",
                        },
                        grid: {
                            display: false,
                            drawTicks: false,
                            drawOnChartArea: false,
                        },
                    },
                }
            }
        };
    },
    mounted() {
        this.renderChart();
    },
    methods: {
        renderChart() {
            if (this.chart) {
                this.chart.destroy();
            }
            this.chart = new Chart(this.$refs.chartCanvas, {
                type: 'line',
                data: this.chartData,
                options: this.options
            });

            this.legendValues = this.chart.data.datasets.map(dataset => ({
                label: dataset.label,
                color: dataset.borderColor
            }));
        },
    },
    watch: {
        chartData: {
            handler() {
                this.renderChart();
            },
            deep: true
        }
    }
};
</script>

<style scoped>
.canvasContainer {
    background: var(--color-background-soft);
    padding: 15px;
    margin: 15px;
    margin-top: 2%;
    border-radius: 15px;
}

canvas {
    display: flex;
    flex-flow: column;
    width: 100%;
    height: 100%;
    max-width: 800px;
    min-height: 400px;
    max-height: 500px;
}
</style>
