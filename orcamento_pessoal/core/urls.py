"""URLs do app core — Orçamento Pessoal."""
from django.urls import path
from core.views import dashboard, income, expenses, investments, goals
from core.api import views as api_views

app_name = 'core'

urlpatterns = [
    # -----------------------------------------------------------------------
    # Dashboard
    # -----------------------------------------------------------------------
    path('', dashboard.DashboardView.as_view(), name='dashboard'),
    path('perfil/', dashboard.ProfileView.as_view(), name='profile'),

    # -----------------------------------------------------------------------
    # Receitas
    # -----------------------------------------------------------------------
    path('receitas/', income.IncomeListView.as_view(), name='income-list'),
    path('receitas/nova/', income.IncomeCreateView.as_view(), name='income-create'),
    path('receitas/<int:pk>/editar/', income.IncomeUpdateView.as_view(), name='income-update'),
    path('receitas/<int:pk>/excluir/', income.IncomeDeleteView.as_view(), name='income-delete'),
    # Categorias de Receita
    path('receitas/categorias/', income.IncomeCategoryListView.as_view(), name='income-category-list'),
    path('receitas/categorias/nova/', income.IncomeCategoryCreateView.as_view(), name='income-category-create'),
    path('receitas/categorias/<int:pk>/editar/', income.IncomeCategoryUpdateView.as_view(), name='income-category-update'),
    path('receitas/categorias/<int:pk>/excluir/', income.IncomeCategoryDeleteView.as_view(), name='income-category-delete'),

    # -----------------------------------------------------------------------
    # Investimentos
    # -----------------------------------------------------------------------
    path('investimentos/', investments.InvestmentListView.as_view(), name='investment-list'),
    path('investimentos/novo/', investments.InvestmentCreateView.as_view(), name='investment-create'),
    path('investimentos/<int:pk>/editar/', investments.InvestmentUpdateView.as_view(), name='investment-update'),
    path('investimentos/<int:pk>/excluir/', investments.InvestmentDeleteView.as_view(), name='investment-delete'),
    path('investimentos/reserva/', investments.EmergencyReserveView.as_view(), name='emergency-reserve'),
    # Categorias de Investimento
    path('investimentos/categorias/', investments.InvestmentCategoryListView.as_view(), name='investment-category-list'),
    path('investimentos/categorias/nova/', investments.InvestmentCategoryCreateView.as_view(), name='investment-category-create'),
    path('investimentos/categorias/<int:pk>/editar/', investments.InvestmentCategoryUpdateView.as_view(), name='investment-category-update'),

    # -----------------------------------------------------------------------
    # Metas
    # -----------------------------------------------------------------------
    path('metas/', goals.GoalListView.as_view(), name='goal-list'),
    path('metas/nova/', goals.GoalCreateView.as_view(), name='goal-create'),
    path('metas/<int:pk>/editar/', goals.GoalUpdateView.as_view(), name='goal-update'),
    path('metas/<int:pk>/excluir/', goals.GoalDeleteView.as_view(), name='goal-delete'),

    # -----------------------------------------------------------------------
    # Estrutura de Gastos
    # -----------------------------------------------------------------------
    path('gastos/', expenses.ExpenseStructureView.as_view(), name='expense-structure'),
    # Grupos
    path('gastos/grupos/novo/', expenses.ExpenseGroupCreateView.as_view(), name='expense-group-create'),
    path('gastos/grupos/<int:pk>/editar/', expenses.ExpenseGroupUpdateView.as_view(), name='expense-group-update'),
    path('gastos/grupos/<int:pk>/excluir/', expenses.ExpenseGroupDeleteView.as_view(), name='expense-group-delete'),
    # Subgrupos
    path('gastos/subgrupos/novo/', expenses.ExpenseSubgroupCreateView.as_view(), name='expense-subgroup-create'),
    path('gastos/subgrupos/<int:pk>/editar/', expenses.ExpenseSubgroupUpdateView.as_view(), name='expense-subgroup-update'),
    path('gastos/subgrupos/<int:pk>/excluir/', expenses.ExpenseSubgroupDeleteView.as_view(), name='expense-subgroup-delete'),
    # Itens
    path('gastos/itens/novo/', expenses.ExpenseItemCreateView.as_view(), name='expense-item-create'),
    path('gastos/itens/<int:pk>/editar/', expenses.ExpenseItemUpdateView.as_view(), name='expense-item-update'),
    path('gastos/itens/<int:pk>/excluir/', expenses.ExpenseItemDeleteView.as_view(), name='expense-item-delete'),
    # Transações
    path('transacoes/', expenses.TransactionListView.as_view(), name='transaction-list'),
    path('transacoes/nova/', expenses.TransactionCreateView.as_view(), name='transaction-create'),
    path('transacoes/<int:pk>/editar/', expenses.TransactionUpdateView.as_view(), name='transaction-update'),
    path('transacoes/<int:pk>/excluir/', expenses.TransactionDeleteView.as_view(), name='transaction-delete'),

    # -----------------------------------------------------------------------
    # API JSON (para os gráficos e AJAX)
    # -----------------------------------------------------------------------
    path('api/dashboard-data/', api_views.DashboardDataView.as_view(), name='api-dashboard-data'),
    path('api/expense-groups/', api_views.ExpenseGroupsDataView.as_view(), name='api-expense-groups'),
    path('api/monthly-comparison/', api_views.MonthlyComparisonView.as_view(), name='api-monthly-comparison'),
    path('api/patrimony-evolution/', api_views.PatrimonyEvolutionView.as_view(), name='api-patrimony-evolution'),
    path('api/items-by-subgroup/', api_views.ItemsBySubgroupView.as_view(), name='api-items-by-subgroup'),
]
