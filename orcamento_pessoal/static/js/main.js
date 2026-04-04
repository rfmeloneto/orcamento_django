/**
 * main.js — Orçamento Pessoal
 * Controla: sidebar, tema, período e utilitários gerais.
 */

'use strict';

// ── Tema claro / escuro ───────────────────────────────────────────────────────
const THEME_KEY = 'orcamento-theme';

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);
}

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const preferred = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  applyTheme(saved || preferred);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

// ── Sidebar ───────────────────────────────────────────────────────────────────
const SIDEBAR_KEY = 'orcamento-sidebar';

function initSidebar() {
  const sidebar  = document.getElementById('sidebar');
  const overlay  = document.getElementById('sidebarOverlay');
  const mainContent = document.getElementById('mainContent');
  if (!sidebar) return;

  // Desktop: restaura estado colapsado
  const collapsed = localStorage.getItem(SIDEBAR_KEY) === 'collapsed';
  if (collapsed && window.innerWidth >= 992) {
    sidebar.classList.add('collapsed');
    document.body.classList.add('sidebar-collapsed');
  }

  // Toggle desktop (botão dentro do sidebar)
  const toggleBtn = document.getElementById('sidebarToggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (window.innerWidth < 992) return;
      const isCollapsed = sidebar.classList.toggle('collapsed');
      document.body.classList.toggle('sidebar-collapsed', isCollapsed);
      localStorage.setItem(SIDEBAR_KEY, isCollapsed ? 'collapsed' : 'open');
    });
  }

  // Toggle mobile (botão hamburguer na topbar)
  const menuBtn = document.getElementById('menuToggle');
  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      if (window.innerWidth >= 992) {
        // No desktop, o botão da topbar também colapsa
        const isCollapsed = sidebar.classList.toggle('collapsed');
        document.body.classList.toggle('sidebar-collapsed', isCollapsed);
        localStorage.setItem(SIDEBAR_KEY, isCollapsed ? 'collapsed' : 'open');
      } else {
        sidebar.classList.toggle('mobile-open');
        overlay.classList.toggle('active');
      }
    });
  }

  // Fecha sidebar mobile ao clicar no overlay
  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('active');
    });
  }

  // Fecha sidebar mobile ao redimensionar para desktop
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 992) {
      sidebar.classList.remove('mobile-open');
      overlay.classList.remove('active');
    }
  });
}

// ── Período (mês/ano) — seletor na topbar ─────────────────────────────────────
function initPeriodSelector() {
  const monthSelect = document.querySelector('.topbar select[name="month"]');
  const yearInput   = document.querySelector('.topbar input[name="year"]');
  if (!monthSelect || !yearInput) return;

  // Preenche mês/ano atual se vazio
  const today = new Date();
  if (!monthSelect.value) monthSelect.value = today.getMonth() + 1;
  if (!yearInput.value)   yearInput.value   = today.getFullYear();
}

// ── Utilitário: formata moeda BRL ────────────────────────────────────────────
window.formatBRL = function (value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
  }).format(value);
};

// ── Dismiss automático das mensagens ────────────────────────────────────────
function initAutoMessages() {
  const alerts = document.querySelectorAll('.messages-container .alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 4500);
  });
}

// ── Confirmação de exclusão com Bootstrap Modal (se disponível) ───────────────
function initDeleteConfirm() {
  // Handled by dedicated confirm_delete.html template
}

// ── Inicialização ─────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initPeriodSelector();
  initAutoMessages();

  // Botão de toggle de tema
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', toggleTheme);
  }

  // Re-inicia ícones Lucide após qualquer inserção dinâmica
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});
