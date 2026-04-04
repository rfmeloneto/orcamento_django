"""
Views do Dashboard e Perfil do usuário.
"""
import datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from core.models import (
    Profile, Income, Investment, EmergencyReserve,
    FinancialGoal, ExpenseGroup, Transaction,
)
from core.forms import ProfileForm


def get_period(request):
    """Extrai ano/mês dos query params, com fallback para o mês atual."""
    today = datetime.date.today()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
    except (ValueError, TypeError):
        year, month = today.year, today.month
    return year, month


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        year, month = get_period(self.request)

        # Receita total do período
        income_total = Income.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        # Gastos totais do período
        expense_total = Transaction.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        # Investimentos do período
        investment_total = Investment.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        # Saldo
        balance = income_total - expense_total - investment_total

        # Grupos com gasto real vs meta
        groups = ExpenseGroup.objects.filter(user=user, is_active=True).order_by('order')
        groups_data = []
        for g in groups:
            spent = g.total_spent(year=year, month=month)
            budget_amount = (g.target_percentage / 100) * income_total if income_total else Decimal('0')
            deviation = spent - budget_amount
            groups_data.append({
                'group': g,
                'spent': spent,
                'budget_amount': budget_amount,
                'deviation': deviation,
                'pct_used': (spent / budget_amount * 100) if budget_amount else Decimal('0'),
            })

        # Metas ativas
        goals = FinancialGoal.objects.filter(user=user, status='active').order_by('term')[:5]

        # Reserva de emergência
        try:
            reserve = user.emergency_reserve
        except EmergencyReserve.DoesNotExist:
            reserve = None

        # Patrimônio total (investimentos + reserva)
        total_invested = Investment.objects.filter(user=user).aggregate(
            total=Sum('current_value')
        )['total'] or Decimal('0')

        ctx.update({
            'year': year,
            'month': month,
            'month_name': datetime.date(year, month, 1).strftime('%B %Y'),
            'income_total': income_total,
            'expense_total': expense_total,
            'investment_total': investment_total,
            'balance': balance,
            'groups_data': groups_data,
            'goals': goals,
            'reserve': reserve,
            'total_invested': total_invested,
            'expense_pct': (expense_total / income_total * 100) if income_total else Decimal('0'),
            'today': datetime.date.today(),
        })
        return ctx


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(user=user)
        ctx['form'] = ProfileForm(instance=profile, user=user)
        ctx['profile'] = profile
        return ctx

    def post(self, request, *args, **kwargs):
        user = request.user
        profile, _ = Profile.objects.get_or_create(user=user)
        form = ProfileForm(request.POST, instance=profile, user=user)
        if form.is_valid():
            form.save()
            form.save_user_data(user)
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('core:profile')
        return self.render_to_response(self.get_context_data(form=form))
