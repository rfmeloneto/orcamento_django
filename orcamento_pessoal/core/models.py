# """
# Modelos do sistema de Orçamento Pessoal.

# Hierarquia de gastos:
#     ExpenseGroup → ExpenseSubgroup → ExpenseItem → Transaction

# Outras entidades:
#     Profile, IncomeCategory, Income,
#     InvestmentCategory, Investment, EmergencyReserve,
#     FinancialGoal
# """
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models import Sum
# from decimal import Decimal
# import datetime


# # ---------------------------------------------------------------------------
# # Perfil do usuário
# # ---------------------------------------------------------------------------

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     monthly_income_target = models.DecimalField(
#         'Renda Mensal Esperada', max_digits=12, decimal_places=2, default=0
#     )
#     currency_symbol = models.CharField('Símbolo da Moeda', max_length=5, default='R$')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Perfil'
#         verbose_name_plural = 'Perfis'

#     def __str__(self):
#         return f'Perfil de {self.user.get_full_name() or self.user.username}'


# # ---------------------------------------------------------------------------
# # Receitas (Incomes)
# # ---------------------------------------------------------------------------

# class IncomeCategory(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_categories')
#     name = models.CharField('Nome', max_length=100)
#     icon = models.CharField('Ícone (Lucide)', max_length=50, default='circle-dollar-sign')
#     is_active = models.BooleanField('Ativo', default=True)

#     class Meta:
#         verbose_name = 'Categoria de Receita'
#         verbose_name_plural = 'Categorias de Receita'
#         ordering = ['name']
#         unique_together = ['user', 'name']

#     def __str__(self):
#         return self.name


# class Income(models.Model):
#     RECURRENCE_CHOICES = [
#         ('none', 'Sem recorrência'),
#         ('monthly', 'Mensal'),
#         ('annual', 'Anual'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
#     category = models.ForeignKey(
#         IncomeCategory, on_delete=models.PROTECT, related_name='incomes',
#         verbose_name='Categoria'
#     )
#     description = models.CharField('Descrição', max_length=255)
#     amount = models.DecimalField('Valor', max_digits=12, decimal_places=2)
#     date = models.DateField('Data')
#     recurrence = models.CharField(
#         'Recorrência', max_length=10, choices=RECURRENCE_CHOICES, default='none'
#     )
#     notes = models.TextField('Observações', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Receita'
#         verbose_name_plural = 'Receitas'
#         ordering = ['-date', '-created_at']

#     def __str__(self):
#         return f'{self.description} — R$ {self.amount}'


# # ---------------------------------------------------------------------------
# # Investimentos
# # ---------------------------------------------------------------------------

# class InvestmentCategory(models.Model):
#     TYPE_CHOICES = [
#         ('fixed', 'Renda Fixa'),
#         ('variable', 'Renda Variável'),
#         ('reserve', 'Reserva de Emergência'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_categories')
#     name = models.CharField('Nome', max_length=100)
#     investment_type = models.CharField('Tipo', max_length=10, choices=TYPE_CHOICES)
#     icon = models.CharField('Ícone (Lucide)', max_length=50, default='trending-up')
#     is_active = models.BooleanField('Ativo', default=True)

#     class Meta:
#         verbose_name = 'Categoria de Investimento'
#         verbose_name_plural = 'Categorias de Investimento'
#         ordering = ['investment_type', 'name']
#         unique_together = ['user', 'name']

#     def __str__(self):
#         return f'{self.name} ({self.get_investment_type_display()})'


# class Investment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
#     category = models.ForeignKey(
#         InvestmentCategory, on_delete=models.PROTECT, related_name='investments',
#         verbose_name='Categoria'
#     )
#     description = models.CharField('Descrição', max_length=255)
#     amount = models.DecimalField('Valor Aplicado', max_digits=12, decimal_places=2)
#     current_value = models.DecimalField(
#         'Valor Atual', max_digits=12, decimal_places=2, null=True, blank=True,
#         help_text='Deixe em branco para usar o valor aplicado'
#     )
#     date = models.DateField('Data')
#     notes = models.TextField('Observações', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Investimento'
#         verbose_name_plural = 'Investimentos'
#         ordering = ['-date', '-created_at']

#     def __str__(self):
#         return f'{self.description} — R$ {self.amount}'

#     @property
#     def effective_value(self):
#         """Retorna valor atual ou o valor aplicado se não informado."""
#         return self.current_value if self.current_value is not None else self.amount

#     @property
#     def gain_loss(self):
#         return self.effective_value - self.amount

#     @property
#     def gain_loss_pct(self):
#         if self.amount == 0:
#             return Decimal('0')
#         return (self.gain_loss / self.amount) * 100


# # ---------------------------------------------------------------------------
# # Reserva de Emergência
# # ---------------------------------------------------------------------------

# class EmergencyReserve(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='emergency_reserve')
#     target_amount = models.DecimalField('Meta da Reserva', max_digits=12, decimal_places=2, default=0)
#     current_amount = models.DecimalField('Valor Atual', max_digits=12, decimal_places=2, default=0)
#     notes = models.TextField('Observações', blank=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Reserva de Emergência'
#         verbose_name_plural = 'Reservas de Emergência'

#     def __str__(self):
#         return f'Reserva de {self.user.username}: R$ {self.current_amount}'

#     @property
#     def progress_pct(self):
#         if not self.target_amount:
#             return Decimal('0')
#         pct = (self.current_amount / self.target_amount) * 100
#         return min(pct, Decimal('100'))

#     @property
#     def remaining(self):
#         return max(self.target_amount - self.current_amount, Decimal('0'))


# # ---------------------------------------------------------------------------
# # Metas Financeiras
# # ---------------------------------------------------------------------------

# class FinancialGoal(models.Model):
#     TERM_CHOICES = [
#         ('short', 'Curto Prazo (até 1 ano)'),
#         ('medium', 'Médio Prazo (1 a 5 anos)'),
#         ('long', 'Longo Prazo (acima de 5 anos)'),
#     ]

#     STATUS_CHOICES = [
#         ('active', 'Ativa'),
#         ('achieved', 'Conquistada'),
#         ('paused', 'Pausada'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_goals')
#     name = models.CharField('Nome da Meta', max_length=150)
#     description = models.TextField('Descrição', blank=True)
#     term = models.CharField('Prazo', max_length=10, choices=TERM_CHOICES)
#     target_amount = models.DecimalField('Valor Alvo', max_digits=12, decimal_places=2)
#     current_amount = models.DecimalField('Valor Acumulado', max_digits=12, decimal_places=2, default=0)
#     target_date = models.DateField('Data Alvo', null=True, blank=True)
#     status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='active')
#     icon = models.CharField('Ícone (Lucide)', max_length=50, default='target')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = 'Meta Financeira'
#         verbose_name_plural = 'Metas Financeiras'
#         ordering = ['term', 'name']

#     def __str__(self):
#         return self.name

#     @property
#     def remaining(self):
#         return max(self.target_amount - self.current_amount, Decimal('0'))

#     @property
#     def progress_pct(self):
#         if not self.target_amount:
#             return Decimal('0')
#         pct = (self.current_amount / self.target_amount) * 100
#         return min(pct, Decimal('100'))

#     @property
#     def months_to_goal(self):
#         """Calcula meses restantes até a data alvo a partir de hoje."""
#         if not self.target_date:
#             return None
#         today = datetime.date.today()
#         if self.target_date <= today:
#             return 0
#         delta = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)
#         return max(delta, 0)

#     @property
#     def monthly_needed(self):
#         """Valor mensal necessário para atingir a meta no prazo."""
#         months = self.months_to_goal
#         if not months:
#             return None
#         remaining = self.remaining
#         if remaining <= 0:
#             return Decimal('0')
#         return remaining / months


# # ---------------------------------------------------------------------------
# # Hierarquia de Gastos: Grupo > Subgrupo > Item > Transação
# # ---------------------------------------------------------------------------

# class ExpenseGroup(models.Model):
#     """
#     Ex: Fixos Essenciais, Fixos Necessários, Variáveis Essenciais, etc.
#     Cada grupo tem uma % alvo do orçamento.
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_groups')
#     name = models.CharField('Nome do Grupo', max_length=100)
#     target_percentage = models.DecimalField(
#         '% Alvo do Orçamento', max_digits=5, decimal_places=2, default=0,
#         help_text='Percentual da renda mensal destinado a este grupo'
#     )
#     color = models.CharField('Cor (hex)', max_length=7, default='#6366f1')
#     icon = models.CharField('Ícone (Lucide)', max_length=50, default='layers')
#     order = models.PositiveSmallIntegerField('Ordem', default=0)
#     is_active = models.BooleanField('Ativo', default=True)

#     class Meta:
#         verbose_name = 'Grupo de Despesa'
#         verbose_name_plural = 'Grupos de Despesa'
#         ordering = ['order', 'name']
#         unique_together = ['user', 'name']

#     def __str__(self):
#         return self.name

#     def total_spent(self, year=None, month=None):
#         """Soma das transações deste grupo no período informado."""
#         qs = Transaction.objects.filter(item__subgroup__group=self)
#         if year and month:
#             qs = qs.filter(date__year=year, date__month=month)
#         return qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')


# class ExpenseSubgroup(models.Model):
#     """
#     Ex: Moradia, Contas Básicas, Saúde (dentro de Fixos Essenciais)
#     """
#     group = models.ForeignKey(
#         ExpenseGroup, on_delete=models.CASCADE, related_name='subgroups',
#         verbose_name='Grupo'
#     )
#     name = models.CharField('Nome do Subgrupo', max_length=100)
#     icon = models.CharField('Ícone (Lucide)', max_length=50, default='tag')
#     order = models.PositiveSmallIntegerField('Ordem', default=0)
#     is_active = models.BooleanField('Ativo', default=True)

#     class Meta:
#         verbose_name = 'Subgrupo de Despesa'
#         verbose_name_plural = 'Subgrupos de Despesa'
#         ordering = ['order', 'name']
#         unique_together = ['group', 'name']

#     def __str__(self):
#         return f'{self.group.name} → {self.name}'

#     def total_spent(self, year=None, month=None):
#         qs = Transaction.objects.filter(item__subgroup=self)
#         if year and month:
#             qs = qs.filter(date__year=year, date__month=month)
#         return qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')


# class ExpenseItem(models.Model):
#     """
#     Ex: Financiamento Imóvel, Condomínio, IPTU (dentro de Moradia)
#     """
#     subgroup = models.ForeignKey(
#         ExpenseSubgroup, on_delete=models.CASCADE, related_name='items',
#         verbose_name='Subgrupo'
#     )
#     name = models.CharField('Nome do Item', max_length=100)
#     is_active = models.BooleanField('Ativo', default=True)

#     class Meta:
#         verbose_name = 'Item de Despesa'
#         verbose_name_plural = 'Itens de Despesa'
#         ordering = ['name']
#         unique_together = ['subgroup', 'name']

#     def __str__(self):
#         return f'{self.subgroup.name} → {self.name}'

#     def total_spent(self, year=None, month=None):
#         qs = self.transactions.all()
#         if year and month:
#             qs = qs.filter(date__year=year, date__month=month)
#         return qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')


# class Transaction(models.Model):
#     """
#     Registro do gasto real. Vinculado a um ExpenseItem.
#     """
#     PAYMENT_CHOICES = [
#         ('cash', 'Dinheiro'),
#         ('debit', 'Débito'),
#         ('credit', 'Crédito'),
#         ('pix', 'Pix'),
#         ('transfer', 'Transferência'),
#         ('other', 'Outro'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     item = models.ForeignKey(
#         ExpenseItem, on_delete=models.PROTECT, related_name='transactions',
#         verbose_name='Item de Despesa'
#     )
#     description = models.CharField('Descrição', max_length=255)
#     amount = models.DecimalField('Valor', max_digits=12, decimal_places=2)
#     date = models.DateField('Data')
#     payment_method = models.CharField(
#         'Forma de Pagamento', max_length=10, choices=PAYMENT_CHOICES, default='pix'
#     )
#     notes = models.TextField('Observações', blank=True)
#     is_recurring = models.BooleanField('É recorrente?', default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = 'Transação'
#         verbose_name_plural = 'Transações'
#         ordering = ['-date', '-created_at']

#     def __str__(self):
#         return f'{self.description} — R$ {self.amount} ({self.date})'

#     @property
#     def group(self):
#         return self.item.subgroup.group

#     @property
#     def subgroup(self):
#         return self.item.subgroup

"""
Modelos do sistema de Orçamento Pessoal.

Hierarquia de gastos:
    ExpenseGroup → ExpenseSubgroup → ExpenseItem → Transaction

Outras entidades:
    Profile, IncomeCategory, Income,
    InvestmentCategory, Investment, EmergencyReserve,
    FinancialGoal
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
import datetime


# ---------------------------------------------------------------------------
# Perfil do usuário
# ---------------------------------------------------------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    monthly_income_target = models.DecimalField(
        'Renda Mensal Esperada', max_digits=12, decimal_places=2, default=0
    )
    currency_symbol = models.CharField('Símbolo da Moeda', max_length=5, default='R$')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.user.get_full_name() or self.user.username}'


# ---------------------------------------------------------------------------
# Receitas (Incomes)
# ---------------------------------------------------------------------------

class IncomeCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_categories')
    name = models.CharField('Nome', max_length=100)
    icon = models.CharField('Ícone (Lucide)', max_length=50, default='circle-dollar-sign')
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Categoria de Receita'
        verbose_name_plural = 'Categorias de Receita'
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name


class Income(models.Model):
    RECURRENCE_CHOICES = [
        ('none', 'Sem recorrência'),
        ('monthly', 'Mensal'),
        ('annual', 'Anual'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    category = models.ForeignKey(
        IncomeCategory, on_delete=models.PROTECT, related_name='incomes',
        verbose_name='Categoria'
    )
    description = models.CharField('Descrição', max_length=255)
    amount = models.DecimalField('Valor', max_digits=12, decimal_places=2)
    date = models.DateField('Data')
    recurrence = models.CharField(
        'Recorrência', max_length=10, choices=RECURRENCE_CHOICES, default='none'
    )
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.description} — R$ {self.amount}'


# ---------------------------------------------------------------------------
# Investimentos
# ---------------------------------------------------------------------------

class InvestmentCategory(models.Model):
    TYPE_CHOICES = [
        ('fixed', 'Renda Fixa'),
        ('variable', 'Renda Variável'),
        ('reserve', 'Reserva de Emergência'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_categories')
    name = models.CharField('Nome', max_length=100)
    investment_type = models.CharField('Tipo', max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField('Ícone (Lucide)', max_length=50, default='trending-up')
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Categoria de Investimento'
        verbose_name_plural = 'Categorias de Investimento'
        ordering = ['investment_type', 'name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f'{self.name} ({self.get_investment_type_display()})'


class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    category = models.ForeignKey(
        InvestmentCategory, on_delete=models.PROTECT, related_name='investments',
        verbose_name='Categoria'
    )
    description = models.CharField('Descrição', max_length=255)
    amount = models.DecimalField('Valor Aplicado', max_digits=12, decimal_places=2)
    current_value = models.DecimalField(
        'Valor Atual', max_digits=12, decimal_places=2, null=True, blank=True,
        help_text='Deixe em branco para usar o valor aplicado'
    )
    date = models.DateField('Data')
    notes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Investimento'
        verbose_name_plural = 'Investimentos'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.description} — R$ {self.amount}'

    @property
    def effective_value(self):
        """Retorna valor atual ou o valor aplicado se não informado."""
        return self.current_value if self.current_value is not None else self.amount

    @property
    def gain_loss(self):
        return self.effective_value - self.amount

    @property
    def gain_loss_pct(self):
        if self.amount == 0:
            return Decimal('0')
        return (self.gain_loss / self.amount) * 100


# ---------------------------------------------------------------------------
# Reserva de Emergência
# ---------------------------------------------------------------------------

class EmergencyReserve(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='emergency_reserve')
    target_amount = models.DecimalField('Meta da Reserva', max_digits=12, decimal_places=2, default=0)
    current_amount = models.DecimalField('Valor Atual', max_digits=12, decimal_places=2, default=0)
    notes = models.TextField('Observações', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reserva de Emergência'
        verbose_name_plural = 'Reservas de Emergência'

    def __str__(self):
        return f'Reserva de {self.user.username}: R$ {self.current_amount}'

    @property
    def progress_pct(self):
        if not self.target_amount:
            return Decimal('0')
        pct = (self.current_amount / self.target_amount) * 100
        return min(pct, Decimal('100'))

    @property
    def remaining(self):
        return max(self.target_amount - self.current_amount, Decimal('0'))


# ---------------------------------------------------------------------------
# Metas Financeiras
# ---------------------------------------------------------------------------

class FinancialGoal(models.Model):
    TERM_CHOICES = [
        ('short', 'Curto Prazo (até 1 ano)'),
        ('medium', 'Médio Prazo (1 a 5 anos)'),
        ('long', 'Longo Prazo (acima de 5 anos)'),
    ]

    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('achieved', 'Conquistada'),
        ('paused', 'Pausada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_goals')
    name = models.CharField('Nome da Meta', max_length=150)
    description = models.TextField('Descrição', blank=True)
    term = models.CharField('Prazo', max_length=10, choices=TERM_CHOICES)
    target_amount = models.DecimalField('Valor Alvo', max_digits=12, decimal_places=2)
    current_amount = models.DecimalField('Valor Acumulado', max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField('Data Alvo', null=True, blank=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='active')
    icon = models.CharField('Ícone (Lucide)', max_length=50, default='target')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Meta Financeira'
        verbose_name_plural = 'Metas Financeiras'
        ordering = ['term', 'name']

    def __str__(self):
        return self.name

    @property
    def remaining(self):
        return max(self.target_amount - self.current_amount, Decimal('0'))

    @property
    def progress_pct(self):
        if not self.target_amount:
            return Decimal('0')
        pct = (self.current_amount / self.target_amount) * 100
        return min(pct, Decimal('100'))

    @property
    def months_to_goal(self):
        """Calcula meses restantes até a data alvo a partir de hoje."""
        if not self.target_date:
            return None
        today = datetime.date.today()
        if self.target_date <= today:
            return 0
        delta = (self.target_date.year - today.year) * 12 + (self.target_date.month - today.month)
        return max(delta, 0)

    @property
    def monthly_needed(self):
        """Valor mensal necessário para atingir a meta no prazo."""
        months = self.months_to_goal
        if not months:
            return None
        remaining = self.remaining
        if remaining <= 0:
            return Decimal('0')
        return remaining / months


# ---------------------------------------------------------------------------
# Hierarquia de Gastos: Grupo > Subgrupo > Item > Transação
# ---------------------------------------------------------------------------

class ExpenseGroup(models.Model):
    """
    Ex: Fixos Essenciais, Fixos Necessários, Variáveis Essenciais, etc.
    Cada grupo tem uma % alvo do orçamento.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_groups')
    name = models.CharField('Nome do Grupo', max_length=100)
    target_percentage = models.DecimalField(
        '% Alvo do Orçamento', max_digits=5, decimal_places=2, default=0,
        help_text='Percentual da renda mensal destinado a este grupo'
    )
    color = models.CharField('Cor (hex)', max_length=7, default='#6366f1')
    icon = models.CharField('Ícone (Lucide)', max_length=50, default='layers')
    order = models.PositiveSmallIntegerField('Ordem', default=0)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Grupo de Despesa'
        verbose_name_plural = 'Grupos de Despesa'
        ordering = ['order', 'name']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

    def total_spent(self, year=None, month=None):
        """Soma das transações deste grupo no período informado."""
        qs = Transaction.objects.filter(item__subgroup__group=self)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')


class ExpenseSubgroup(models.Model):
    """
    Ex: Moradia, Contas Básicas, Saúde (dentro de Fixos Essenciais)
    """
    group = models.ForeignKey(
        ExpenseGroup, on_delete=models.CASCADE, related_name='subgroups',
        verbose_name='Grupo'
    )
    name = models.CharField('Nome do Subgrupo', max_length=100)
    icon = models.CharField('Ícone (Lucide)', max_length=50, default='tag')
    order = models.PositiveSmallIntegerField('Ordem', default=0)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Subgrupo de Despesa'
        verbose_name_plural = 'Subgrupos de Despesa'
        ordering = ['order', 'name']
        unique_together = ['group', 'name']

    def __str__(self):
        return f'{self.group.name} → {self.name}'

    def total_spent(self, year=None, month=None):
        qs = Transaction.objects.filter(item__subgroup=self)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')


class ExpenseItem(models.Model):
    """
    Ex: Financiamento Imóvel, Condomínio, IPTU (dentro de Moradia)
    """
    subgroup = models.ForeignKey(
        ExpenseSubgroup, on_delete=models.CASCADE, related_name='items',
        verbose_name='Subgrupo'
    )
    name = models.CharField('Nome do Item', max_length=100)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Item de Despesa'
        verbose_name_plural = 'Itens de Despesa'
        ordering = ['name']
        unique_together = ['subgroup', 'name']

    def __str__(self):
        return f'{self.subgroup.name} → {self.name}'

    def total_spent(self, year=None, month=None):
        qs = self.transactions.all()
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('amount'))['total'] or Decimal('0')


class Transaction(models.Model):
    """
    Registro do gasto real. Vinculado a um ExpenseItem.
    """
    PAYMENT_CHOICES = [
        ('cash', 'Dinheiro'),
        ('debit', 'Débito'),
        ('credit', 'Crédito'),
        ('pix', 'Pix'),
        ('transfer', 'Transferência'),
        ('other', 'Outro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    item = models.ForeignKey(
        ExpenseItem, on_delete=models.PROTECT, related_name='transactions',
        verbose_name='Item de Despesa'
    )
    description = models.CharField('Descrição', max_length=255)
    amount = models.DecimalField('Valor', max_digits=12, decimal_places=2)
    date = models.DateField('Data')
    payment_method = models.CharField(
        'Forma de Pagamento', max_length=10, choices=PAYMENT_CHOICES, default='pix'
    )
    notes = models.TextField('Observações', blank=True)
    is_recurring = models.BooleanField('É recorrente?', default=False)
    is_projected = models.BooleanField(
        'É projeção automática?', default=False,
        help_text='Marcado automaticamente pelo sistema para despesas recorrentes projetadas'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.description} — R$ {self.amount} ({self.date})'

    @property
    def group(self):
        return self.item.subgroup.group

    @property
    def subgroup(self):
        return self.item.subgroup