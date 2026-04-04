/**
 * transactions.js — Orçamento Pessoal
 * Funcionalidades de UX para o formulário de transação:
 *  - Máscara de valor monetário (BRL)
 *  - Data padrão = hoje
 *  - Highlight do grupo/subgrupo do item selecionado
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
  initAmountMask();
  initDefaultDate();
  initItemSelect();
});

// ── Máscara monetária no campo "Valor" ────────────────────────────────────────
function initAmountMask() {
  const amountInput = document.querySelector('input[name="amount"]');
  if (!amountInput) return;

  amountInput.addEventListener('blur', () => {
    const raw = parseFloat(amountInput.value);
    if (!isNaN(raw) && raw > 0) {
      // Mantém apenas 2 casas decimais
      amountInput.value = raw.toFixed(2);
    }
  });

  // Aceita apenas números e ponto/vírgula
  amountInput.addEventListener('keypress', (e) => {
    const char = String.fromCharCode(e.which);
    if (!/[\d.,]/.test(char)) e.preventDefault();
  });
}

// ── Data padrão = hoje ────────────────────────────────────────────────────────
function initDefaultDate() {
  const dateInput = document.querySelector('input[name="date"]');
  if (!dateInput || dateInput.value) return;

  const today = new Date();
  const yyyy = today.getFullYear();
  const mm   = String(today.getMonth() + 1).padStart(2, '0');
  const dd   = String(today.getDate()).padStart(2, '0');
  dateInput.value = `${yyyy}-${mm}-${dd}`;
}

// ── Enriquece o select de item com informação do subgrupo/grupo ───────────────
function initItemSelect() {
  const itemSelect = document.querySelector('select[name="item"]');
  if (!itemSelect) return;

  // Adiciona um preview textual abaixo do select mostrando Grupo > Subgrupo
  const preview = document.createElement('small');
  preview.className = 'text-muted d-block mt-1';
  preview.id = 'item-breadcrumb';
  itemSelect.parentNode.appendChild(preview);

  function updatePreview() {
    const selected = itemSelect.options[itemSelect.selectedIndex];
    if (!selected || !selected.value) {
      preview.textContent = '';
      return;
    }
    // O text do option no Django vem como "Subgrupo → Item"
    // mas o __str__ do ExpenseItem retorna "Subgrupo → Item"
    // Vamos apenas mostrar o texto completo do option
    preview.innerHTML = `<i data-lucide="corner-down-right" style="width:12px;height:12px;"></i> ${selected.text}`;
    if (typeof lucide !== 'undefined') lucide.createIcons();
  }

  itemSelect.addEventListener('change', updatePreview);
  updatePreview();
}
