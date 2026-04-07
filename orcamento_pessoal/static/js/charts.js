/**
 * charts.js — Orçamento Pessoal
 * Inicializa e atualiza todos os gráficos Chart.js do dashboard.
 * Chamado a partir do template dashboard/index.html com:
 *   initDashboardCharts(year, month)
 */

'use strict';

// ── Helpers ──────────────────────────────────────────────────────────────────

/** Lê as CSS vars do tema atual para manter os gráficos consistentes. */
function getCSSVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

/** Configurações globais Chart.js aplicadas ao inicializar. */
function setupChartDefaults() {
  const textColor = getCSSVar('--color-text-2');
  const gridColor = getCSSVar('--color-border');
  const fontFamily = "'DM Sans', sans-serif";

  Chart.defaults.color = textColor;
  Chart.defaults.font.family = fontFamily;
  Chart.defaults.font.size = 12;

  Chart.defaults.plugins.legend.display = false;
  Chart.defaults.plugins.tooltip.backgroundColor = getCSSVar('--color-surface');
  Chart.defaults.plugins.tooltip.titleColor = getCSSVar('--color-text');
  Chart.defaults.plugins.tooltip.bodyColor = getCSSVar('--color-text-2');
  Chart.defaults.plugins.tooltip.borderColor = getCSSVar('--color-border');
  Chart.defaults.plugins.tooltip.borderWidth = 1;
  Chart.defaults.plugins.tooltip.padding = 10;
  Chart.defaults.plugins.tooltip.cornerRadius = 8;
  Chart.defaults.plugins.tooltip.callbacks.label = function (ctx) {
    const val = typeof ctx.parsed === 'object' ? ctx.parsed.y ?? ctx.parsed : ctx.parsed;
    return ' ' + window.formatBRL(val);
  };

  Chart.defaults.scale.grid.color = gridColor;
  Chart.defaults.scale.ticks.color = textColor;
}

// Referências dos gráficos para permitir destruição e recriação
let donutChart = null;
let barChart   = null;
let lineChart  = null;

// ── Donut: Distribuição por Grupo ─────────────────────────────────────────────
async function loadDonutChart(year, month) {
  const res  = await fetch(`/api/expense-groups/?year=${year}&month=${month}`);
  const data = await res.json();

  const ctx = document.getElementById('donutChart');
  if (!ctx) return;

  if (donutChart) donutChart.destroy();

  donutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: data.labels,
      datasets: [
        {
          label: 'Gasto Real',
          data: data.spent,
          backgroundColor: data.colors.map(c => c + 'CC'),  // 80% alpha
          borderColor: data.colors,
          borderWidth: 2,
          hoverOffset: 6,
        },
      ],
    },
    options: {
      responsive: true,
      cutout: '68%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.label}: ${window.formatBRL(ctx.parsed)}`,
          },
        },
      },
      animation: { animateRotate: true, duration: 800 },
    },
  });

  // Legenda customizada
  const legend = document.getElementById('donutLegend');
  if (legend) {
    legend.innerHTML = data.labels.map((label, i) => `
      <div class="chart-legend-item">
        <span class="chart-legend-dot" style="background:${data.colors[i]};"></span>
        <span>${label}</span>
      </div>
    `).join('');
  }
}

// ── Barras: Comparativo Receita vs Gastos ─────────────────────────────────────
async function loadBarChart() {
  const res  = await fetch('/api/monthly-comparison/?months=6');
  const data = await res.json();

  const ctx = document.getElementById('barChart');
  if (!ctx) return;

  if (barChart) barChart.destroy();

  const primary = getCSSVar('--color-primary');
  const danger  = getCSSVar('--color-danger');

  barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [
        {
          label: 'Receita',
          data: data.income,
          backgroundColor: primary + '33',
          borderColor: primary,
          borderWidth: 2,
          borderRadius: 6,
          borderSkipped: false,
        },
        {
          label: 'Gastos',
          data: data.expense,
          backgroundColor: danger + '33',
          borderColor: danger,
          borderWidth: 2,
          borderRadius: 6,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'end',
          labels: {
            usePointStyle: true,
            pointStyle: 'rectRounded',
            padding: 16,
            font: { size: 12 },
          },
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: ${window.formatBRL(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: { grid: { display: false }, border: { display: false } },
        y: {
          border: { display: false },
          ticks: {
            callback: (val) => 'R$ ' + Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 0 }),
          },
        },
      },
      animation: { duration: 700 },
    },
  });
}

// ── Linha: Evolução do Patrimônio ─────────────────────────────────────────────
async function loadLineChart() {
  const res  = await fetch('/api/patrimony-evolution/?months=12');
  const data = await res.json();

  const ctx = document.getElementById('lineChart');
  if (!ctx) return;

  if (lineChart) lineChart.destroy();

  const primary = getCSSVar('--color-primary');

  lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [
        {
          label: 'Patrimônio',
          data: data.patrimony,
          borderColor: primary,
          borderWidth: 2.5,
          pointBackgroundColor: primary,
          pointRadius: 4,
          pointHoverRadius: 6,
          fill: true,
          backgroundColor: (ctx) => {
            const chart = ctx.chart;
            const { ctx: c, chartArea } = chart;
            if (!chartArea) return 'transparent';
            const gradient = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
            gradient.addColorStop(0, primary + '44');
            gradient.addColorStop(1, primary + '00');
            return gradient;
          },
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` Patrimônio: ${window.formatBRL(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: { grid: { display: false }, border: { display: false } },
        y: {
          border: { display: false },
          ticks: {
            callback: (val) => 'R$ ' + Number(val).toLocaleString('pt-BR', { minimumFractionDigits: 0 }),
          },
        },
      },
      animation: { duration: 900 },
    },
  });
}

// ── Ponto de entrada ──────────────────────────────────────────────────────────
window.initDashboardCharts = async function (year, month) {
  setupChartDefaults();
  await Promise.all([
    loadDonutChart(year, month),
    loadBarChart(),
    loadLineChart(),
  ]);
};

// Re-renderiza os gráficos ao trocar o tema (Chart.js não reage automaticamente)
const originalToggle = window.toggleTheme;
document.addEventListener('DOMContentLoaded', () => {
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      // Aguarda a transição de tema e re-inicializa os gráficos
      setTimeout(() => {
        setupChartDefaults();
        if (typeof CURRENT_YEAR !== 'undefined') {
          loadDonutChart(CURRENT_YEAR, CURRENT_MONTH);
          loadBarChart();
          loadLineChart();
        }
      }, 350);
    });
  }
});
