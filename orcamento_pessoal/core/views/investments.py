"""Views de Investimentos, Categorias e Reserva de Emergência."""
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect

from core.models import Investment, InvestmentCategory, EmergencyReserve
from core.forms import InvestmentForm, InvestmentCategoryForm, EmergencyReserveForm


class InvestmentListView(LoginRequiredMixin, ListView):
    model = Investment
    template_name = 'investments/list.html'
    context_object_name = 'investments'
    paginate_by = 20

    def get_queryset(self):
        qs = Investment.objects.filter(user=self.request.user).select_related('category')
        inv_type = self.request.GET.get('type')
        if inv_type:
            qs = qs.filter(category__investment_type=inv_type)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Totais por tipo
        base_qs = Investment.objects.filter(user=user)
        fixed_total = base_qs.filter(category__investment_type='fixed').aggregate(
            total=Sum('current_value')
        )['total'] or Decimal('0')
        variable_total = base_qs.filter(category__investment_type='variable').aggregate(
            total=Sum('current_value')
        )['total'] or Decimal('0')
        reserve_total = base_qs.filter(category__investment_type='reserve').aggregate(
            total=Sum('current_value')
        )['total'] or Decimal('0')
        grand_total = fixed_total + variable_total + reserve_total

        try:
            reserve = user.emergency_reserve
        except EmergencyReserve.DoesNotExist:
            reserve = None

        ctx.update({
            'fixed_total': fixed_total,
            'variable_total': variable_total,
            'reserve_total': reserve_total,
            'grand_total': grand_total,
            'reserve': reserve,
        })
        return ctx


class InvestmentCreateView(LoginRequiredMixin, CreateView):
    model = Investment
    form_class = InvestmentForm
    template_name = 'investments/form.html'
    success_url = reverse_lazy('core:investment-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Investimento registrado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Novo Investimento'
        ctx['action'] = 'Registrar'
        return ctx


class InvestmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Investment
    form_class = InvestmentForm
    template_name = 'investments/form.html'
    success_url = reverse_lazy('core:investment-list')

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Investimento atualizado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Investimento'
        ctx['action'] = 'Salvar'
        return ctx


class InvestmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Investment
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:investment-list')

    def get_queryset(self):
        return Investment.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Investimento excluído.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Investimento'
        ctx['message'] = f'Deseja excluir "{self.object.description}"?'
        ctx['back_url'] = reverse_lazy('core:investment-list')
        return ctx


class EmergencyReserveView(LoginRequiredMixin, TemplateView):
    template_name = 'investments/reserve.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        reserve, _ = EmergencyReserve.objects.get_or_create(user=self.request.user)
        ctx['form'] = EmergencyReserveForm(instance=reserve)
        ctx['reserve'] = reserve
        return ctx

    def post(self, request, *args, **kwargs):
        reserve, _ = EmergencyReserve.objects.get_or_create(user=request.user)
        form = EmergencyReserveForm(request.POST, instance=reserve)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva de emergência atualizada!')
            return redirect('core:emergency-reserve')
        return self.render_to_response(self.get_context_data(form=form))


# ---------------------------------------------------------------------------
# Categorias de Investimento
# ---------------------------------------------------------------------------

class InvestmentCategoryListView(LoginRequiredMixin, ListView):
    model = InvestmentCategory
    template_name = 'investments/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return InvestmentCategory.objects.filter(user=self.request.user)


class InvestmentCategoryCreateView(LoginRequiredMixin, CreateView):
    model = InvestmentCategory
    form_class = InvestmentCategoryForm
    template_name = 'investments/category_form.html'
    success_url = reverse_lazy('core:investment-category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Categoria de investimento criada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Nova Categoria de Investimento'
        return ctx


class InvestmentCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = InvestmentCategory
    form_class = InvestmentCategoryForm
    template_name = 'investments/category_form.html'
    success_url = reverse_lazy('core:investment-category-list')

    def get_queryset(self):
        return InvestmentCategory.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Categoria de Investimento'
        return ctx
