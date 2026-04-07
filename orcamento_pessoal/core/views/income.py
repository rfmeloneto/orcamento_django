"""Views de Receitas (Incomes) e suas Categorias."""
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.models import Income, IncomeCategory
from core.forms import IncomeForm, IncomeCategoryForm


class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income/list.html'
    context_object_name = 'incomes'
    paginate_by = 20

    def get_queryset(self):
        qs = Income.objects.filter(user=self.request.user).select_related('category')
        # Filtros
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        category = self.request.GET.get('category')
        if year:
            qs = qs.filter(date__year=year)
        if month:
            qs = qs.filter(date__month=month)
        if category:
            qs = qs.filter(category_id=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = datetime.date.today()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))

        total = Income.objects.filter(
            user=user, date__year=year, date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        ctx.update({
            'categories': IncomeCategory.objects.filter(user=user, is_active=True),
            'total': total,
            'year': year,
            'month': month,
        })
        return ctx


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/form.html'
    success_url = reverse_lazy('core:income-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Receita registrada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Nova Receita'
        ctx['action'] = 'Registrar'
        return ctx


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/form.html'
    success_url = reverse_lazy('core:income-list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Receita atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Receita'
        ctx['action'] = 'Salvar'
        return ctx


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:income-list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Receita excluída.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Receita'
        ctx['message'] = f'Deseja excluir a receita "{self.object.description}"?'
        ctx['back_url'] = reverse_lazy('core:income-list')
        return ctx


# ---------------------------------------------------------------------------
# Categorias de Receita
# ---------------------------------------------------------------------------

class IncomeCategoryListView(LoginRequiredMixin, ListView):
    model = IncomeCategory
    template_name = 'income/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)


class IncomeCategoryCreateView(LoginRequiredMixin, CreateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = 'income/category_form.html'
    success_url = reverse_lazy('core:income-category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Categoria criada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Nova Categoria de Receita'
        return ctx


class IncomeCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = IncomeCategory
    form_class = IncomeCategoryForm
    template_name = 'income/category_form.html'
    success_url = reverse_lazy('core:income-category-list')

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Categoria de Receita'
        return ctx


class IncomeCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = IncomeCategory
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:income-category-list')

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Categoria excluída.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Categoria'
        ctx['message'] = f'Deseja excluir a categoria "{self.object.name}"?'
        ctx['back_url'] = reverse_lazy('core:income-category-list')
        return ctx
