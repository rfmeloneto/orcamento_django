"""
Admin do sistema de Orçamento Pessoal.
Registra todos os modelos com configurações aprimoradas para uso no painel.
"""
from django.contrib import admin
from .models import (
    Profile, IncomeCategory, Income,
    InvestmentCategory, Investment, EmergencyReserve,
    FinancialGoal,
    ExpenseGroup, ExpenseSubgroup, ExpenseItem, Transaction,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'monthly_income_target', 'currency_symbol']
    search_fields = ['user__username', 'user__email']


# ---------------------------------------------------------------------------
# Receitas
# ---------------------------------------------------------------------------

@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active']
    list_filter = ['is_active', 'user']
    search_fields = ['name']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'amount', 'date', 'recurrence', 'user']
    list_filter = ['category', 'recurrence', 'date', 'user']
    search_fields = ['description']
    date_hierarchy = 'date'


# ---------------------------------------------------------------------------
# Investimentos
# ---------------------------------------------------------------------------

@admin.register(InvestmentCategory)
class InvestmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'investment_type', 'user', 'is_active']
    list_filter = ['investment_type', 'is_active']


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['description', 'category', 'amount', 'current_value', 'date', 'user']
    list_filter = ['category__investment_type', 'date']
    date_hierarchy = 'date'


@admin.register(EmergencyReserve)
class EmergencyReserveAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_amount', 'target_amount']


# ---------------------------------------------------------------------------
# Metas
# ---------------------------------------------------------------------------

@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ['name', 'term', 'target_amount', 'current_amount', 'status', 'user']
    list_filter = ['term', 'status', 'user']
    search_fields = ['name']


# ---------------------------------------------------------------------------
# Estrutura de Gastos
# ---------------------------------------------------------------------------

class ExpenseSubgroupInline(admin.TabularInline):
    model = ExpenseSubgroup
    extra = 1


class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 1


@admin.register(ExpenseGroup)
class ExpenseGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'target_percentage', 'color', 'order', 'user', 'is_active']
    list_filter = ['is_active', 'user']
    inlines = [ExpenseSubgroupInline]
    ordering = ['order']


@admin.register(ExpenseSubgroup)
class ExpenseSubgroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'order', 'is_active']
    list_filter = ['group', 'is_active']
    inlines = [ExpenseItemInline]


@admin.register(ExpenseItem)
class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'subgroup', 'is_active']
    list_filter = ['subgroup__group', 'is_active']
    search_fields = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'item', 'amount', 'date', 'payment_method', 'user']
    list_filter = ['payment_method', 'date', 'item__subgroup__group', 'user']
    search_fields = ['description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
