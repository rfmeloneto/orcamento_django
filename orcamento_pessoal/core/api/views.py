"""
Endpoints JSON consumidos pelos gráficos Chart.js.
Todas as views exigem autenticação e retornam apenas dados do usuário logado.
"""
import datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View

from core.models import (
    Income, Transaction, Investment, ExpenseGroup, EmergencyReserve
)

MONTH_NAMES = [
    '', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
]


def _get_period(request):
    today = datetime.date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
    except (ValueError, TypeError):
        year, month = today.year, today.month
    return year, month


class DashboardDataView(LoginRequiredMixin, View):
    """Resumo financeiro do período: receita, gastos, investimentos, saldo."""

    def get(self, request, *args, **kwargs):
        user = request.user
        year, month = _get_period(request)

        income = Income.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        expense = Transaction.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        invested = Investment.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        return JsonResponse({
            'income': float(income),
            'expense': float(expense),
            'invested': float(invested),
            'balance': float(income - expense - invested),
            'expense_pct': float(expense / income * 100) if income else 0,
        })


class ExpenseGroupsDataView(LoginRequiredMixin, View):
    """
    Dados para o gráfico de pizza/donut:
    distribuição de gastos por grupo no período.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        year, month = _get_period(request)

        groups = ExpenseGroup.objects.filter(user=user, is_active=True).order_by('order')

        # Receita do período para calcular % alvo em R$
        income = Income.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        labels, spent_data, budget_data, colors = [], [], [], []

        for g in groups:
            spent = g.total_spent(year=year, month=month)
            budget = (g.target_percentage / 100) * income if income else Decimal('0')
            labels.append(g.name)
            spent_data.append(float(spent))
            budget_data.append(float(budget))
            colors.append(g.color)

        return JsonResponse({
            'labels': labels,
            'spent': spent_data,
            'budget': budget_data,
            'colors': colors,
        })


class MonthlyComparisonView(LoginRequiredMixin, View):
    """
    Gráfico de barras: comparativo dos últimos 6 meses.
    Retorna receita e gastos por mês.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        today = datetime.date.today()
        months_count = int(request.GET.get('months', 6))

        labels, income_data, expense_data = [], [], []

        for i in range(months_count - 1, -1, -1):
            # Volta i meses a partir de hoje
            month_date = (today.replace(day=1) - datetime.timedelta(days=1) * 0)
            # Calcular mês correto retroativamente
            total_months = today.month - 1 - i
            year = today.year + total_months // 12
            month = total_months % 12 + 1
            if total_months < 0:
                year = today.year - 1 + (total_months + 1) // 12
                month = 12 + (total_months + 1) % 12

            inc = Income.objects.filter(
                user=user, date__year=year, date__month=month
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            exp = Transaction.objects.filter(
                user=user, date__year=year, date__month=month
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

            labels.append(f"{MONTH_NAMES[month]}/{str(year)[2:]}")
            income_data.append(float(inc))
            expense_data.append(float(exp))

        return JsonResponse({
            'labels': labels,
            'income': income_data,
            'expense': expense_data,
        })


class PatrimonyEvolutionView(LoginRequiredMixin, View):
    """
    Gráfico de linha: evolução do patrimônio total
    (soma dos investimentos acumulados mês a mês).
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        today = datetime.date.today()
        months_count = int(request.GET.get('months', 12))

        labels, patrimony_data = [], []

        for i in range(months_count - 1, -1, -1):
            total_months = today.month - 1 - i
            year = today.year + total_months // 12
            month = total_months % 12 + 1
            if total_months < 0:
                year = today.year - 1 + (total_months + 1) // 12
                month = 12 + (total_months + 1) % 12

            # Patrimônio acumulado até aquele mês
            invested = Investment.objects.filter(
                user=user,
                date__year__lte=year,
            ).filter(
                date__month__lte=month
            ).aggregate(total=Sum('current_value'))['total'] or Decimal('0')

            labels.append(f"{MONTH_NAMES[month]}/{str(year)[2:]}")
            patrimony_data.append(float(invested))

        return JsonResponse({
            'labels': labels,
            'patrimony': patrimony_data,
        })


class ItemsBySubgroupView(LoginRequiredMixin, View):
    """
    Retorna itens de despesa para um subgrupo específico (usado no form de transação via AJAX).
    """

    def get(self, request, *args, **kwargs):
        from core.models import ExpenseItem
        subgroup_id = request.GET.get('subgroup_id')
        user = request.user

        if not subgroup_id:
            return JsonResponse({'items': []})

        items = ExpenseItem.objects.filter(
            subgroup_id=subgroup_id,
            subgroup__group__user=user,
            is_active=True,
        ).values('id', 'name')

        return JsonResponse({'items': list(items)})
