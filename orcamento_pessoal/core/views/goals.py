"""Views de Metas Financeiras."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.models import FinancialGoal
from core.forms import FinancialGoalForm


class GoalListView(LoginRequiredMixin, ListView):
    model = FinancialGoal
    template_name = 'goals/list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user).order_by('term', 'name')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        goals = self.get_queryset()
        short = goals.filter(term='short')
        medium = goals.filter(term='medium')
        long = goals.filter(term='long')
        ctx['short_goals'] = short
        ctx['medium_goals'] = medium
        ctx['long_goals'] = long
        # Seções ordenadas para o template iterar
        ctx['term_sections'] = [
            ('short', 'Curto Prazo (até 1 ano)', short),
            ('medium', 'Médio Prazo (1 a 5 anos)', medium),
            ('long', 'Longo Prazo (acima de 5 anos)', long),
        ]
        return ctx


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = FinancialGoal
    form_class = FinancialGoalForm
    template_name = 'goals/form.html'
    success_url = reverse_lazy('core:goal-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Meta criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Nova Meta Financeira'
        ctx['action'] = 'Criar Meta'
        return ctx


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = FinancialGoal
    form_class = FinancialGoalForm
    template_name = 'goals/form.html'
    success_url = reverse_lazy('core:goal-list')

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Meta atualizada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Meta'
        ctx['action'] = 'Salvar'
        return ctx


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = FinancialGoal
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:goal-list')

    def get_queryset(self):
        return FinancialGoal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Meta excluída.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Meta'
        ctx['message'] = f'Deseja excluir a meta "{self.object.name}"?'
        ctx['back_url'] = reverse_lazy('core:goal-list')
        return ctx
