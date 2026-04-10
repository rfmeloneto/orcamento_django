
# """
# Views de Gastos: Grupos, Subgrupos, Itens e Transações.
# """
# import datetime
# import json
# from decimal import Decimal, InvalidOperation

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
# from django.db import transaction as db_transaction
# from django.db.models import Sum
# from django.http import JsonResponse
# from django.urls import reverse_lazy
# from django.views import View
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

# from core.models import (
#     ExpenseGroup, ExpenseSubgroup, ExpenseItem, Transaction, Income
# )
# from core.forms import (
#     ExpenseGroupForm, ExpenseSubgroupForm, ExpenseItemForm, TransactionForm
# )


# # ---------------------------------------------------------------------------
# # Estrutura (Grupos > Subgrupos > Itens) — view unificada
# # ---------------------------------------------------------------------------

# class ExpenseStructureView(LoginRequiredMixin, TemplateView):
#     template_name = 'expenses/structure.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         user = self.request.user
#         today = datetime.date.today()

#         groups = (
#             ExpenseGroup.objects
#             .filter(user=user)
#             .prefetch_related('subgroups__items')
#             .order_by('order')
#         )
#         income_month = Income.objects.filter(
#             user=user, date__year=today.year, date__month=today.month
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

#         ctx.update({
#             'groups': groups,
#             'income_month': income_month,
#             'group_form': ExpenseGroupForm(),
#             'subgroup_form': ExpenseSubgroupForm(user=user),
#             'item_form': ExpenseItemForm(user=user),
#         })
#         return ctx


# # ---------------------------------------------------------------------------
# # ExpenseGroup CRUD
# # ---------------------------------------------------------------------------

# class ExpenseGroupCreateView(LoginRequiredMixin, CreateView):
#     model = ExpenseGroup
#     form_class = ExpenseGroupForm
#     template_name = 'expenses/group_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(self.request, 'Grupo criado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Novo Grupo de Despesa'
#         ctx['action'] = 'Criar'
#         return ctx


# class ExpenseGroupUpdateView(LoginRequiredMixin, UpdateView):
#     model = ExpenseGroup
#     form_class = ExpenseGroupForm
#     template_name = 'expenses/group_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseGroup.objects.filter(user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Grupo atualizado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Grupo'
#         ctx['action'] = 'Salvar'
#         return ctx


# class ExpenseGroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = ExpenseGroup
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseGroup.objects.filter(user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Grupo excluído.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Grupo'
#         ctx['message'] = f'Deseja excluir o grupo "{self.object.name}" e todos seus subgrupos e itens?'
#         ctx['back_url'] = reverse_lazy('core:expense-structure')
#         return ctx


# # ---------------------------------------------------------------------------
# # ExpenseSubgroup CRUD
# # ---------------------------------------------------------------------------

# class ExpenseSubgroupCreateView(LoginRequiredMixin, CreateView):
#     model = ExpenseSubgroup
#     form_class = ExpenseSubgroupForm
#     template_name = 'expenses/subgroup_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Subgrupo criado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Novo Subgrupo'
#         ctx['action'] = 'Criar'
#         return ctx


# class ExpenseSubgroupUpdateView(LoginRequiredMixin, UpdateView):
#     model = ExpenseSubgroup
#     form_class = ExpenseSubgroupForm
#     template_name = 'expenses/subgroup_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseSubgroup.objects.filter(group__user=self.request.user)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Subgrupo atualizado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Subgrupo'
#         ctx['action'] = 'Salvar'
#         return ctx


# class ExpenseSubgroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = ExpenseSubgroup
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseSubgroup.objects.filter(group__user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Subgrupo excluído.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Subgrupo'
#         ctx['message'] = f'Deseja excluir o subgrupo "{self.object.name}"?'
#         ctx['back_url'] = reverse_lazy('core:expense-structure')
#         return ctx


# # ---------------------------------------------------------------------------
# # ExpenseItem CRUD
# # ---------------------------------------------------------------------------

# class ExpenseItemCreateView(LoginRequiredMixin, CreateView):
#     model = ExpenseItem
#     form_class = ExpenseItemForm
#     template_name = 'expenses/item_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Item criado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Novo Item de Despesa'
#         ctx['action'] = 'Criar'
#         return ctx


# class ExpenseItemUpdateView(LoginRequiredMixin, UpdateView):
#     model = ExpenseItem
#     form_class = ExpenseItemForm
#     template_name = 'expenses/item_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseItem.objects.filter(subgroup__group__user=self.request.user)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Item atualizado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Item'
#         ctx['action'] = 'Salvar'
#         return ctx


# class ExpenseItemDeleteView(LoginRequiredMixin, DeleteView):
#     model = ExpenseItem
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseItem.objects.filter(subgroup__group__user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Item excluído.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Item'
#         ctx['message'] = f'Deseja excluir o item "{self.object.name}"?'
#         ctx['back_url'] = reverse_lazy('core:expense-structure')
#         return ctx


# # ---------------------------------------------------------------------------
# # Transações — listagem
# # ---------------------------------------------------------------------------

# class TransactionListView(LoginRequiredMixin, ListView):
#     model = Transaction
#     template_name = 'expenses/transactions.html'
#     context_object_name = 'transactions'
#     paginate_by = 25

#     def get_queryset(self):
#         user = self.request.user
#         today = datetime.date.today()
#         year  = int(self.request.GET.get('year',  today.year))
#         month = int(self.request.GET.get('month', today.month))

#         qs = Transaction.objects.filter(
#             user=user, date__year=year, date__month=month
#         ).select_related('item__subgroup__group').order_by('-date', '-created_at')

#         group_id = self.request.GET.get('group')
#         if group_id:
#             qs = qs.filter(item__subgroup__group_id=group_id)

#         return qs

#     def get_context_data(self, **kwargs):
#         ctx   = super().get_context_data(**kwargs)
#         user  = self.request.user
#         today = datetime.date.today()
#         year  = int(self.request.GET.get('year',  today.year))
#         month = int(self.request.GET.get('month', today.month))

#         total = self.get_queryset().aggregate(total=Sum('amount'))['total'] or Decimal('0')

#         ctx.update({
#             'year':           year,
#             'month':          month,
#             'total':          total,
#             'groups':         ExpenseGroup.objects.filter(user=user, is_active=True).order_by('order'),
#             'selected_group': self.request.GET.get('group'),
#         })
#         return ctx


# # ---------------------------------------------------------------------------
# # Transação — criação via Progressive Disclosure (nova UX)
# # ---------------------------------------------------------------------------

# def _build_hierarchy(user):
#     """
#     Retorna a hierarquia Grupo > Subgrupo > Item como lista JSON-serializável,
#     apenas com dados ativos do usuário logado.
#     """
#     groups = (
#         ExpenseGroup.objects
#         .filter(user=user, is_active=True)
#         .prefetch_related('subgroups__items')
#         .order_by('order')
#     )
#     result = []
#     for g in groups:
#         subgroups = []
#         for sg in g.subgroups.filter(is_active=True).order_by('order', 'name'):
#             items = [
#                 {'id': it.pk, 'name': it.name}
#                 for it in sg.items.filter(is_active=True).order_by('name')
#             ]
#             subgroups.append({
#                 'id':   sg.pk,
#                 'name': sg.name,
#                 'icon': sg.icon,
#                 'items': items,
#             })
#         result.append({
#             'id':        g.pk,
#             'name':      g.name,
#             'icon':      g.icon,
#             'color':     g.color,
#             'subgroups': subgroups,
#         })
#     return result


# class TransactionCreateView(LoginRequiredMixin, TemplateView):
#     """
#     Renderiza o formulário de criação com Progressive Disclosure.
#     O submit real é feito por TransactionBulkCreateView.
#     """
#     template_name = 'expenses/transaction_form.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title']          = 'Nova Transação'
#         ctx['edit_mode']      = False
#         ctx['expense_groups'] = (
#             ExpenseGroup.objects
#             .filter(user=self.request.user, is_active=True)
#             .prefetch_related('subgroups')
#             .order_by('order')
#         )
#         ctx['hierarchy_json'] = json.dumps(_build_hierarchy(self.request.user), ensure_ascii=False)
#         return ctx


# # ---------------------------------------------------------------------------
# # Transação — bulk create (recebe POST do formulário PD)
# # ---------------------------------------------------------------------------

# PAYMENT_MAP = {
#     'Pix':           'pix',
#     'Crédito':       'credit',
#     'Débito':        'debit',
#     'Dinheiro':      'cash',
#     'Transferência': 'transfer',
#     'Outro':         'other',
# }


# class TransactionBulkCreateView(LoginRequiredMixin, View):
#     """
#     Recebe o POST do formulário de Progressive Disclosure e cria uma
#     Transaction por cada entrada (data + valor) informada.
#     """

#     def post(self, request, *args, **kwargs):
#         user = request.user

#         try:
#             item_id     = int(request.POST.get('item_id', 0))
#             entries_raw = request.POST.get('entries_json', '[]')
#             description = request.POST.get('description', '').strip()
#             notes       = request.POST.get('notes', '').strip()
#             payment_raw = request.POST.get('payment_method', 'Pix')
#             is_recurring = request.POST.get('is_recurring', '0') == '1'

#             entries = json.loads(entries_raw)
#             payment = PAYMENT_MAP.get(payment_raw, 'pix')

#             # valida item pertence ao usuário
#             item = ExpenseItem.objects.get(
#                 pk=item_id,
#                 subgroup__group__user=user,
#                 is_active=True,
#             )

#             description = description or item.name

#             with db_transaction.atomic():
#                 created = []
#                 for e in entries:
#                     amount_val = e.get('amount', '')
#                     try:
#                         amount = Decimal(str(amount_val))
#                     except InvalidOperation:
#                         continue
#                     if amount <= 0:
#                         continue

#                     date_str = e.get('date', '')
#                     try:
#                         date = datetime.date.fromisoformat(date_str)
#                     except (ValueError, TypeError):
#                         date = datetime.date.today()

#                     t = Transaction.objects.create(
#                         user=user,
#                         item=item,
#                         description=description,
#                         amount=amount,
#                         date=date,
#                         payment_method=payment,
#                         notes=notes,
#                         is_recurring=is_recurring,
#                     )
#                     created.append(t)

#             if not created:
#                 messages.error(request, 'Nenhum valor válido informado.')
#                 from django.shortcuts import redirect
#                 return redirect('core:transaction-create')

#             n = len(created)
#             messages.success(
#                 request,
#                 f'{n} transação{"ões" if n > 1 else ""} registrada{"s" if n > 1 else ""}!'
#             )

#         except ExpenseItem.DoesNotExist:
#             messages.error(request, 'Item de despesa não encontrado.')
#         except (json.JSONDecodeError, ValueError, KeyError) as exc:
#             messages.error(request, f'Dados inválidos: {exc}')

#         from django.shortcuts import redirect
#         return redirect('core:transaction-list')


# # ---------------------------------------------------------------------------
# # Transação — edição e exclusão (fluxo clássico mantido)
# # ---------------------------------------------------------------------------

# class TransactionUpdateView(LoginRequiredMixin, UpdateView):
#     model = Transaction
#     form_class = TransactionForm
#     template_name = 'expenses/transaction_form.html'
#     success_url = reverse_lazy('core:transaction-list')

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Transação atualizada!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title']     = 'Editar Transação'
#         ctx['action']    = 'Salvar'
#         ctx['edit_mode'] = True   # usa o formulário clássico no template
#         return ctx


# class TransactionDeleteView(LoginRequiredMixin, DeleteView):
#     model = Transaction
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:transaction-list')

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Transação excluída.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title']    = 'Excluir Transação'
#         ctx['message']  = f'Deseja excluir "{self.object.description}"?'
#         ctx['back_url'] = reverse_lazy('core:transaction-list')
#         return ctx


# """
# Views de Gastos: Grupos, Subgrupos, Itens e Transações.
# """
# import datetime
# from decimal import Decimal

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib import messages
# from django.db.models import Sum
# from django.urls import reverse_lazy
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

# from core.models import (
#     ExpenseGroup, ExpenseSubgroup, ExpenseItem, Transaction, Income
# )
# from core.forms import (
#     ExpenseGroupForm, ExpenseSubgroupForm, ExpenseItemForm, TransactionForm
# )


# # ---------------------------------------------------------------------------
# # Estrutura (Grupos > Subgrupos > Itens) — view unificada
# # ---------------------------------------------------------------------------

# class ExpenseStructureView(LoginRequiredMixin, TemplateView):
#     template_name = 'expenses/structure.html'

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         user = self.request.user
#         today = datetime.date.today()

#         groups = (
#             ExpenseGroup.objects
#             .filter(user=user)
#             .prefetch_related('subgroups__items')
#             .order_by('order')
#         )
#         # Receita mensal para calcular % alvo
#         income_month = Income.objects.filter(
#             user=user, date__year=today.year, date__month=today.month
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

#         ctx.update({
#             'groups': groups,
#             'income_month': income_month,
#             'group_form': ExpenseGroupForm(),
#             'subgroup_form': ExpenseSubgroupForm(user=user),
#             'item_form': ExpenseItemForm(user=user),
#         })
#         return ctx


# # ---------------------------------------------------------------------------
# # ExpenseGroup CRUD
# # ---------------------------------------------------------------------------

# class ExpenseGroupCreateView(LoginRequiredMixin, CreateView):
#     model = ExpenseGroup
#     form_class = ExpenseGroupForm
#     template_name = 'expenses/group_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(self.request, 'Grupo criado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Novo Grupo de Despesa'
#         ctx['action'] = 'Criar'
#         return ctx


# class ExpenseGroupUpdateView(LoginRequiredMixin, UpdateView):
#     model = ExpenseGroup
#     form_class = ExpenseGroupForm
#     template_name = 'expenses/group_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseGroup.objects.filter(user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Grupo atualizado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Grupo'
#         ctx['action'] = 'Salvar'
#         return ctx


# class ExpenseGroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = ExpenseGroup
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseGroup.objects.filter(user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Grupo excluído.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Grupo'
#         ctx['message'] = f'Deseja excluir o grupo "{self.object.name}" e todos seus subgrupos e itens?'
#         ctx['back_url'] = reverse_lazy('core:expense-structure')
#         return ctx


# # ---------------------------------------------------------------------------
# # ExpenseSubgroup CRUD
# # ---------------------------------------------------------------------------

# class ExpenseSubgroupCreateView(LoginRequiredMixin, CreateView):
#     model = ExpenseSubgroup
#     form_class = ExpenseSubgroupForm
#     template_name = 'expenses/subgroup_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Subgrupo criado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Novo Subgrupo'
#         ctx['action'] = 'Criar'
#         return ctx


# class ExpenseSubgroupUpdateView(LoginRequiredMixin, UpdateView):
#     model = ExpenseSubgroup
#     form_class = ExpenseSubgroupForm
#     template_name = 'expenses/subgroup_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseSubgroup.objects.filter(group__user=self.request.user)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Subgrupo atualizado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Subgrupo'
#         ctx['action'] = 'Salvar'
#         return ctx


# class ExpenseSubgroupDeleteView(LoginRequiredMixin, DeleteView):
#     model = ExpenseSubgroup
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseSubgroup.objects.filter(group__user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Subgrupo excluído.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Subgrupo'
#         ctx['message'] = f'Deseja excluir o subgrupo "{self.object.name}"?'
#         ctx['back_url'] = reverse_lazy('core:expense-structure')
#         return ctx


# # ---------------------------------------------------------------------------
# # ExpenseItem CRUD
# # ---------------------------------------------------------------------------

# class ExpenseItemCreateView(LoginRequiredMixin, CreateView):
#     model = ExpenseItem
#     form_class = ExpenseItemForm
#     template_name = 'expenses/item_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Item criado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Novo Item de Despesa'
#         ctx['action'] = 'Criar'
#         return ctx


# class ExpenseItemUpdateView(LoginRequiredMixin, UpdateView):
#     model = ExpenseItem
#     form_class = ExpenseItemForm
#     template_name = 'expenses/item_form.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseItem.objects.filter(subgroup__group__user=self.request.user)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Item atualizado!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Item'
#         ctx['action'] = 'Salvar'
#         return ctx


# class ExpenseItemDeleteView(LoginRequiredMixin, DeleteView):
#     model = ExpenseItem
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:expense-structure')

#     def get_queryset(self):
#         return ExpenseItem.objects.filter(subgroup__group__user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Item excluído.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Item'
#         ctx['message'] = f'Deseja excluir o item "{self.object.name}"?'
#         ctx['back_url'] = reverse_lazy('core:expense-structure')
#         return ctx


# # ---------------------------------------------------------------------------
# # Transações
# # ---------------------------------------------------------------------------

# class TransactionListView(LoginRequiredMixin, ListView):
#     model = Transaction
#     template_name = 'expenses/transactions.html'
#     context_object_name = 'transactions'
#     paginate_by = 25

#     def get_queryset(self):
#         user = self.request.user
#         today = datetime.date.today()
#         year = int(self.request.GET.get('year', today.year))
#         month = int(self.request.GET.get('month', today.month))

#         qs = Transaction.objects.filter(
#             user=user, date__year=year, date__month=month
#         ).select_related('item__subgroup__group').order_by('-date', '-created_at')

#         group_id = self.request.GET.get('group')
#         if group_id:
#             qs = qs.filter(item__subgroup__group_id=group_id)

#         return qs

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         user = self.request.user
#         today = datetime.date.today()
#         year = int(self.request.GET.get('year', today.year))
#         month = int(self.request.GET.get('month', today.month))

#         total = self.get_queryset().aggregate(total=Sum('amount'))['total'] or Decimal('0')

#         ctx.update({
#             'year': year,
#             'month': month,
#             'total': total,
#             'groups': ExpenseGroup.objects.filter(user=user, is_active=True).order_by('order'),
#             'selected_group': self.request.GET.get('group'),
#         })
#         return ctx


# class TransactionCreateView(LoginRequiredMixin, CreateView):
#     model = Transaction
#     form_class = TransactionForm
#     template_name = 'expenses/transaction_form.html'
#     success_url = reverse_lazy('core:transaction-list')

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(self.request, 'Transação registrada!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Nova Transação'
#         ctx['action'] = 'Registrar'
#         return ctx


# class TransactionUpdateView(LoginRequiredMixin, UpdateView):
#     model = Transaction
#     form_class = TransactionForm
#     template_name = 'expenses/transaction_form.html'
#     success_url = reverse_lazy('core:transaction-list')

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         messages.success(self.request, 'Transação atualizada!')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Editar Transação'
#         ctx['action'] = 'Salvar'
#         return ctx


# class TransactionDeleteView(LoginRequiredMixin, DeleteView):
#     model = Transaction
#     template_name = 'confirm_delete.html'
#     success_url = reverse_lazy('core:transaction-list')

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, 'Transação excluída.')
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['title'] = 'Excluir Transação'
#         ctx['message'] = f'Deseja excluir "{self.object.description}"?'
#         ctx['back_url'] = reverse_lazy('core:transaction-list')
#         return ctx


"""
Views de Gastos: Grupos, Subgrupos, Itens e Transações.
"""
import datetime
import json
from decimal import Decimal, InvalidOperation

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction as db_transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from core.models import (
    ExpenseGroup, ExpenseSubgroup, ExpenseItem, Transaction, Income
)
from core.forms import (
    ExpenseGroupForm, ExpenseSubgroupForm, ExpenseItemForm, TransactionForm
)
from core.services import project_recurring


# ---------------------------------------------------------------------------
# Estrutura (Grupos > Subgrupos > Itens) — view unificada
# ---------------------------------------------------------------------------

class ExpenseStructureView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/structure.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = datetime.date.today()

        groups = (
            ExpenseGroup.objects
            .filter(user=user)
            .prefetch_related('subgroups__items')
            .order_by('order')
        )
        income_month = Income.objects.filter(
            user=user, date__year=today.year, date__month=today.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        ctx.update({
            'groups': groups,
            'income_month': income_month,
            'group_form': ExpenseGroupForm(),
            'subgroup_form': ExpenseSubgroupForm(user=user),
            'item_form': ExpenseItemForm(user=user),
        })
        return ctx


# ---------------------------------------------------------------------------
# ExpenseGroup CRUD
# ---------------------------------------------------------------------------

class ExpenseGroupCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseGroup
    form_class = ExpenseGroupForm
    template_name = 'expenses/group_form.html'
    success_url = reverse_lazy('core:expense-structure')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Grupo criado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Novo Grupo de Despesa'
        ctx['action'] = 'Criar'
        return ctx


class ExpenseGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseGroup
    form_class = ExpenseGroupForm
    template_name = 'expenses/group_form.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_queryset(self):
        return ExpenseGroup.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Grupo atualizado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Grupo'
        ctx['action'] = 'Salvar'
        return ctx


class ExpenseGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseGroup
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_queryset(self):
        return ExpenseGroup.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Grupo excluído.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Grupo'
        ctx['message'] = f'Deseja excluir o grupo "{self.object.name}" e todos seus subgrupos e itens?'
        ctx['back_url'] = reverse_lazy('core:expense-structure')
        return ctx


# ---------------------------------------------------------------------------
# ExpenseSubgroup CRUD
# ---------------------------------------------------------------------------

class ExpenseSubgroupCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseSubgroup
    form_class = ExpenseSubgroupForm
    template_name = 'expenses/subgroup_form.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Subgrupo criado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Novo Subgrupo'
        ctx['action'] = 'Criar'
        return ctx


class ExpenseSubgroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseSubgroup
    form_class = ExpenseSubgroupForm
    template_name = 'expenses/subgroup_form.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_queryset(self):
        return ExpenseSubgroup.objects.filter(group__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Subgrupo atualizado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Subgrupo'
        ctx['action'] = 'Salvar'
        return ctx


class ExpenseSubgroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseSubgroup
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_queryset(self):
        return ExpenseSubgroup.objects.filter(group__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Subgrupo excluído.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Subgrupo'
        ctx['message'] = f'Deseja excluir o subgrupo "{self.object.name}"?'
        ctx['back_url'] = reverse_lazy('core:expense-structure')
        return ctx


# ---------------------------------------------------------------------------
# ExpenseItem CRUD
# ---------------------------------------------------------------------------

class ExpenseItemCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseItem
    form_class = ExpenseItemForm
    template_name = 'expenses/item_form.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Item criado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Novo Item de Despesa'
        ctx['action'] = 'Criar'
        return ctx


class ExpenseItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseItem
    form_class = ExpenseItemForm
    template_name = 'expenses/item_form.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_queryset(self):
        return ExpenseItem.objects.filter(subgroup__group__user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Item atualizado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Editar Item'
        ctx['action'] = 'Salvar'
        return ctx


class ExpenseItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseItem
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:expense-structure')

    def get_queryset(self):
        return ExpenseItem.objects.filter(subgroup__group__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Item excluído.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Excluir Item'
        ctx['message'] = f'Deseja excluir o item "{self.object.name}"?'
        ctx['back_url'] = reverse_lazy('core:expense-structure')
        return ctx


# ---------------------------------------------------------------------------
# Transações — listagem
# ---------------------------------------------------------------------------

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'expenses/transactions.html'
    context_object_name = 'transactions'
    paginate_by = 25

    def get_queryset(self):
        user = self.request.user
        today = datetime.date.today()
        year  = int(self.request.GET.get('year',  today.year))
        month = int(self.request.GET.get('month', today.month))

        qs = Transaction.objects.filter(
            user=user, date__year=year, date__month=month
        ).select_related('item__subgroup__group').order_by('-date', '-created_at')

        group_id = self.request.GET.get('group')
        if group_id:
            qs = qs.filter(item__subgroup__group_id=group_id)

        return qs

    def get_context_data(self, **kwargs):
        ctx   = super().get_context_data(**kwargs)
        user  = self.request.user
        today = datetime.date.today()
        year  = int(self.request.GET.get('year',  today.year))
        month = int(self.request.GET.get('month', today.month))

        total = self.get_queryset().aggregate(total=Sum('amount'))['total'] or Decimal('0')

        ctx.update({
            'year':           year,
            'month':          month,
            'total':          total,
            'groups':         ExpenseGroup.objects.filter(user=user, is_active=True).order_by('order'),
            'selected_group': self.request.GET.get('group'),
        })
        return ctx


# ---------------------------------------------------------------------------
# Transação — criação via Progressive Disclosure (nova UX)
# ---------------------------------------------------------------------------

def _build_hierarchy(user):
    """
    Retorna a hierarquia Grupo > Subgrupo > Item como lista JSON-serializável,
    apenas com dados ativos do usuário logado.
    """
    groups = (
        ExpenseGroup.objects
        .filter(user=user, is_active=True)
        .prefetch_related('subgroups__items')
        .order_by('order')
    )
    result = []
    for g in groups:
        subgroups = []
        for sg in g.subgroups.filter(is_active=True).order_by('order', 'name'):
            items = [
                {'id': it.pk, 'name': it.name}
                for it in sg.items.filter(is_active=True).order_by('name')
            ]
            subgroups.append({
                'id':   sg.pk,
                'name': sg.name,
                'icon': sg.icon,
                'items': items,
            })
        result.append({
            'id':        g.pk,
            'name':      g.name,
            'icon':      g.icon,
            'color':     g.color,
            'subgroups': subgroups,
        })
    return result


class TransactionCreateView(LoginRequiredMixin, TemplateView):
    """
    Renderiza o formulário de criação com Progressive Disclosure.
    O submit real é feito por TransactionBulkCreateView.
    """
    template_name = 'expenses/transaction_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']          = 'Nova Transação'
        ctx['edit_mode']      = False
        ctx['expense_groups'] = (
            ExpenseGroup.objects
            .filter(user=self.request.user, is_active=True)
            .prefetch_related('subgroups')
            .order_by('order')
        )
        ctx['hierarchy_json'] = json.dumps(_build_hierarchy(self.request.user), ensure_ascii=False)
        return ctx


# ---------------------------------------------------------------------------
# Transação — bulk create (recebe POST do formulário PD)
# ---------------------------------------------------------------------------

PAYMENT_MAP = {
    'Pix':           'pix',
    'Crédito':       'credit',
    'Débito':        'debit',
    'Dinheiro':      'cash',
    'Transferência': 'transfer',
    'Outro':         'other',
}


class TransactionBulkCreateView(LoginRequiredMixin, View):
    """
    Recebe o POST do formulário de Progressive Disclosure e cria uma
    Transaction por cada entrada (data + valor) informada.
    """

    def post(self, request, *args, **kwargs):
        user = request.user

        try:
            item_id     = int(request.POST.get('item_id', 0))
            entries_raw = request.POST.get('entries_json', '[]')
            description = request.POST.get('description', '').strip()
            notes       = request.POST.get('notes', '').strip()
            payment_raw = request.POST.get('payment_method', 'Pix')
            is_recurring = request.POST.get('is_recurring', '0') == '1'

            entries = json.loads(entries_raw)
            payment = PAYMENT_MAP.get(payment_raw, 'pix')

            # valida item pertence ao usuário
            item = ExpenseItem.objects.get(
                pk=item_id,
                subgroup__group__user=user,
                is_active=True,
            )

            description = description or item.name

            with db_transaction.atomic():
                created = []
                for e in entries:
                    amount_val = e.get('amount', '')
                    try:
                        amount = Decimal(str(amount_val))
                    except InvalidOperation:
                        continue
                    if amount <= 0:
                        continue

                    date_str = e.get('date', '')
                    try:
                        date = datetime.date.fromisoformat(date_str)
                    except (ValueError, TypeError):
                        date = datetime.date.today()

                    t = Transaction.objects.create(
                        user=user,
                        item=item,
                        description=description,
                        amount=amount,
                        date=date,
                        payment_method=payment,
                        notes=notes,
                        is_recurring=is_recurring,
                        is_projected=False,
                    )
                    created.append(t)

                # Projeta meses futuros para cada transação recorrente criada
                for t in created:
                    project_recurring(t)

            if not created:
                messages.error(request, 'Nenhum valor válido informado.')
                from django.shortcuts import redirect
                return redirect('core:transaction-create')

            n = len(created)
            messages.success(
                request,
                f'{n} transação{"ões" if n > 1 else ""} registrada{"s" if n > 1 else ""}!'
            )

        except ExpenseItem.DoesNotExist:
            messages.error(request, 'Item de despesa não encontrado.')
        except (json.JSONDecodeError, ValueError, KeyError) as exc:
            messages.error(request, f'Dados inválidos: {exc}')

        from django.shortcuts import redirect
        return redirect('core:transaction-list')


# ---------------------------------------------------------------------------
# Transação — edição e exclusão (fluxo clássico mantido)
# ---------------------------------------------------------------------------

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'expenses/transaction_form.html'
    success_url = reverse_lazy('core:transaction-list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        transaction = self.object
        # Se a transação é recorrente e real, reaplica a projeção a partir deste mês
        if transaction.is_recurring and not transaction.is_projected:
            project_recurring(transaction)
        messages.success(self.request, 'Transação atualizada!')
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']     = 'Editar Transação'
        ctx['action']    = 'Salvar'
        ctx['edit_mode'] = True   # usa o formulário clássico no template
        return ctx


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('core:transaction-list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Transação excluída.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title']    = 'Excluir Transação'
        ctx['message']  = f'Deseja excluir "{self.object.description}"?'
        ctx['back_url'] = reverse_lazy('core:transaction-list')
        return ctx