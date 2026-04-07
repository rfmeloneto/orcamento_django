"""
Formulários do sistema de Orçamento Pessoal.
Todos os forms herdam de ModelForm e filtram querysets pelo usuário logado.
"""
from django import forms
from django.contrib.auth.models import User
from .models import (
    Profile, Income, IncomeCategory,
    Investment, InvestmentCategory, EmergencyReserve,
    FinancialGoal,
    ExpenseGroup, ExpenseSubgroup, ExpenseItem, Transaction,
)


class DateInput(forms.DateInput):
    """Widget com type=date para melhor UX em browsers modernos."""
    input_type = 'date'


# ---------------------------------------------------------------------------
# Perfil
# ---------------------------------------------------------------------------

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', max_length=150, required=False)
    last_name = forms.CharField(label='Sobrenome', max_length=150, required=False)
    email = forms.EmailField(label='E-mail', required=False)

    class Meta:
        model = Profile
        fields = ['monthly_income_target', 'currency_symbol']
        labels = {
            'monthly_income_target': 'Renda Mensal Esperada (R$)',
            'currency_symbol': 'Símbolo da Moeda',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save_user_data(self, user):
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        user.save()


# ---------------------------------------------------------------------------
# Receitas
# ---------------------------------------------------------------------------

class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['name', 'icon']
        labels = {'name': 'Nome', 'icon': 'Ícone'}
        widgets = {'icon': forms.TextInput(attrs={'placeholder': 'Ex: briefcase'})}


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'description', 'amount', 'date', 'recurrence', 'notes']
        labels = {
            'category': 'Categoria',
            'description': 'Descrição',
            'amount': 'Valor (R$)',
            'date': 'Data',
            'recurrence': 'Recorrência',
            'notes': 'Observações',
        }
        widgets = {
            'date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = IncomeCategory.objects.filter(user=user, is_active=True)


# ---------------------------------------------------------------------------
# Investimentos
# ---------------------------------------------------------------------------

class InvestmentCategoryForm(forms.ModelForm):
    class Meta:
        model = InvestmentCategory
        fields = ['name', 'investment_type', 'icon']
        labels = {
            'name': 'Nome',
            'investment_type': 'Tipo',
            'icon': 'Ícone',
        }


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['category', 'description', 'amount', 'current_value', 'date', 'notes']
        labels = {
            'category': 'Categoria',
            'description': 'Descrição',
            'amount': 'Valor Aplicado (R$)',
            'current_value': 'Valor Atual (R$)',
            'date': 'Data',
            'notes': 'Observações',
        }
        widgets = {
            'date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'current_value': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = InvestmentCategory.objects.filter(user=user, is_active=True)


class EmergencyReserveForm(forms.ModelForm):
    class Meta:
        model = EmergencyReserve
        fields = ['target_amount', 'current_amount', 'notes']
        labels = {
            'target_amount': 'Meta da Reserva (R$)',
            'current_amount': 'Valor Atual (R$)',
            'notes': 'Observações',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'target_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'current_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


# ---------------------------------------------------------------------------
# Metas
# ---------------------------------------------------------------------------

class FinancialGoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name', 'description', 'term', 'target_amount', 'current_amount', 'target_date', 'status', 'icon']
        labels = {
            'name': 'Nome da Meta',
            'description': 'Descrição',
            'term': 'Prazo',
            'target_amount': 'Valor Alvo (R$)',
            'current_amount': 'Valor Acumulado (R$)',
            'target_date': 'Data Alvo',
            'status': 'Status',
            'icon': 'Ícone',
        }
        widgets = {
            'target_date': DateInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
            'target_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'current_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ex: target, home, car, plane'}),
        }


# ---------------------------------------------------------------------------
# Estrutura de Gastos
# ---------------------------------------------------------------------------

class ExpenseGroupForm(forms.ModelForm):
    class Meta:
        model = ExpenseGroup
        fields = ['name', 'target_percentage', 'color', 'icon', 'order']
        labels = {
            'name': 'Nome do Grupo',
            'target_percentage': '% Alvo do Orçamento',
            'color': 'Cor',
            'icon': 'Ícone',
            'order': 'Ordem',
        }
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ex: home, shield-check'}),
            'target_percentage': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '100'}),
        }


class ExpenseSubgroupForm(forms.ModelForm):
    class Meta:
        model = ExpenseSubgroup
        fields = ['group', 'name', 'icon', 'order']
        labels = {
            'group': 'Grupo',
            'name': 'Nome do Subgrupo',
            'icon': 'Ícone',
            'order': 'Ordem',
        }
        widgets = {
            'icon': forms.TextInput(attrs={'placeholder': 'Ex: home, tag'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = ExpenseGroup.objects.filter(user=user, is_active=True)


class ExpenseItemForm(forms.ModelForm):
    class Meta:
        model = ExpenseItem
        fields = ['subgroup', 'name']
        labels = {'subgroup': 'Subgrupo', 'name': 'Nome do Item'}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subgroup'].queryset = ExpenseSubgroup.objects.filter(
                group__user=user, is_active=True
            ).select_related('group')


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'description', 'amount', 'date', 'payment_method', 'is_recurring', 'notes']
        labels = {
            'item': 'Categoria / Item',
            'description': 'Descrição',
            'amount': 'Valor (R$)',
            'date': 'Data',
            'payment_method': 'Forma de Pagamento',
            'is_recurring': 'Gasto Recorrente?',
            'notes': 'Observações',
        }
        widgets = {
            'date': DateInput(),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['item'].queryset = (
                ExpenseItem.objects.filter(
                    subgroup__group__user=user,
                    is_active=True,
                    subgroup__is_active=True,
                    subgroup__group__is_active=True,
                )
                .select_related('subgroup', 'subgroup__group')
                .order_by('subgroup__group__order', 'subgroup__name', 'name')
            )
