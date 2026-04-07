"""
Signals do sistema.
Ao criar um novo usuário:
  1. Cria o Profile vinculado.
  2. Cria a EmergencyReserve.
  3. Popula as categorias-padrão de receita, investimento e a hierarquia de gastos.
"""
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import (
    Profile, EmergencyReserve,
    IncomeCategory, InvestmentCategory,
    ExpenseGroup, ExpenseSubgroup, ExpenseItem,
)

# Estrutura padrão de grupos/subgrupos/itens
DEFAULT_EXPENSE_STRUCTURE = [
    {
        'name': 'Fixos Essenciais',
        'target_percentage': 35,
        'color': '#ef4444',
        'icon': 'home',
        'order': 1,
        'subgroups': [
            {
                'name': 'Moradia',
                'icon': 'building-2',
                'items': ['Financiamento Imóvel', 'Condomínio', 'IPTU', 'Aluguel'],
            },
            {
                'name': 'Contas Básicas',
                'icon': 'zap',
                'items': ['Energia', 'Água', 'Gás', 'Internet'],
            },
            {
                'name': 'Saúde',
                'icon': 'heart-pulse',
                'items': ['Plano de Saúde', 'Medicamento de Uso Contínuo'],
            },
            {
                'name': 'Educação',
                'icon': 'graduation-cap',
                'items': ['Escola', 'Faculdade'],
            },
        ],
    },
    {
        'name': 'Fixos Necessários',
        'target_percentage': 15,
        'color': '#f97316',
        'icon': 'shield-check',
        'order': 2,
        'subgroups': [
            {
                'name': 'Transporte',
                'icon': 'car',
                'items': ['Seguro Obrigatório (DPVAT)', 'IPVA', 'Licenciamento', 'Seguro do Carro'],
            },
            {
                'name': 'Cursos',
                'icon': 'book-open',
                'items': ['Idiomas', 'Música', 'Cultura'],
            },
            {
                'name': 'Saúde',
                'icon': 'dumbbell',
                'items': ['Academia', 'Esporte'],
            },
        ],
    },
    {
        'name': 'Variáveis Essenciais',
        'target_percentage': 20,
        'color': '#eab308',
        'icon': 'shopping-cart',
        'order': 3,
        'subgroups': [
            {
                'name': 'Alimentação',
                'icon': 'shopping-basket',
                'items': ['Mercado', 'Feira', 'Padaria'],
            },
            {
                'name': 'Transporte',
                'icon': 'fuel',
                'items': ['Combustível', 'Manutenção do Carro'],
            },
            {
                'name': 'Saúde',
                'icon': 'pill',
                'items': ['Medicamentos', 'Consultas Médicas', 'Exames'],
            },
            {
                'name': 'Consumo',
                'icon': 'package',
                'items': ['Cosméticos de Uso Contínuo', 'Vestuário Básico', 'Higiene Pessoal'],
            },
            {
                'name': 'Serviços',
                'icon': 'wrench',
                'items': ['Limpeza de Ar-Condicionado', 'Limpeza de Sofá'],
            },
        ],
    },
    {
        'name': 'Variáveis Necessários',
        'target_percentage': 15,
        'color': '#22c55e',
        'icon': 'layers',
        'order': 4,
        'subgroups': [
            {
                'name': 'Transporte',
                'icon': 'car-taxi-front',
                'items': ['Uber', 'Táxi', 'Ônibus/Metrô'],
            },
            {
                'name': 'Alimentação',
                'icon': 'utensils',
                'items': ['Restaurante', 'Suplementos Alimentares'],
            },
            {
                'name': 'Diversão e Cultura',
                'icon': 'gamepad-2',
                'items': ['Livros', 'Brinquedos', 'Jogos', 'Streaming'],
            },
            {
                'name': 'Cuidado Pessoal',
                'icon': 'scissors',
                'items': ['Corte de Cabelo', 'Sobrancelha', 'Manicure', 'Cosméticos'],
            },
            {
                'name': 'Casa',
                'icon': 'sofa',
                'items': ['Móveis', 'Utensílios', 'Eletrodomésticos', 'Enxoval'],
            },
            {
                'name': 'Manutenção',
                'icon': 'hammer',
                'items': ['Reforma', 'Pintura', 'Reparos Gerais'],
            },
            {
                'name': 'Cursos',
                'icon': 'monitor',
                'items': ['Cursos Online', 'Cursos Extras'],
            },
            {
                'name': 'Consumo',
                'icon': 'pencil',
                'items': ['Papelaria', 'Itens de Escritório'],
            },
        ],
    },
    {
        'name': 'Prazeres',
        'target_percentage': 10,
        'color': '#a855f7',
        'icon': 'sparkles',
        'order': 5,
        'subgroups': [
            {
                'name': 'Alimentação',
                'icon': 'pizza',
                'items': ['Lanches', 'Delivery', 'Café'],
            },
            {
                'name': 'Lazer',
                'icon': 'ticket',
                'items': ['Cinema', 'Teatro', 'Shows', 'Passeios', 'Viagens'],
            },
            {
                'name': 'Cuidado Pessoal',
                'icon': 'sparkle',
                'items': ['Salão Extra', 'Procedimentos Estéticos', 'Massagem'],
            },
            {
                'name': 'Casa',
                'icon': 'lamp',
                'items': ['Decoração', 'Utensílios Extra'],
            },
        ],
    },
    {
        'name': 'Eventuais',
        'target_percentage': 5,
        'color': '#64748b',
        'icon': 'calendar-clock',
        'order': 6,
        'subgroups': [
            {
                'name': 'Conserto e Manutenção',
                'icon': 'tool',
                'items': ['Conserto Casa', 'Conserto Carro', 'Conserto Eletrônicos'],
            },
            {
                'name': 'Datas Comemorativas',
                'icon': 'gift',
                'items': ['Presentes', 'Festas', 'Natal', 'Aniversários'],
            },
            {
                'name': 'Educação',
                'icon': 'backpack',
                'items': ['Material Escolar', 'Uniformes', 'Livros Didáticos'],
            },
        ],
    },
]

DEFAULT_INCOME_CATEGORIES = [
    {'name': 'Salário', 'icon': 'briefcase'},
    {'name': '13º Salário', 'icon': 'gift'},
    {'name': 'Férias', 'icon': 'sun'},
    {'name': 'Freelance', 'icon': 'laptop'},
    {'name': 'Aluguel Recebido', 'icon': 'key'},
    {'name': 'Dividendos', 'icon': 'trending-up'},
    {'name': 'Outros', 'icon': 'circle-plus'},
]

DEFAULT_INVESTMENT_CATEGORIES = [
    {'name': 'Poupança', 'investment_type': 'fixed', 'icon': 'piggy-bank'},
    {'name': 'CDB', 'investment_type': 'fixed', 'icon': 'landmark'},
    {'name': 'Tesouro Direto', 'investment_type': 'fixed', 'icon': 'shield'},
    {'name': 'LCI / LCA', 'investment_type': 'fixed', 'icon': 'file-text'},
    {'name': 'Ações', 'investment_type': 'variable', 'icon': 'trending-up'},
    {'name': 'FIIs (Fundos Imobiliários)', 'investment_type': 'variable', 'icon': 'building'},
    {'name': 'Criptomoedas', 'investment_type': 'variable', 'icon': 'bitcoin'},
    {'name': 'Reserva de Emergência', 'investment_type': 'reserve', 'icon': 'life-buoy'},
]


@receiver(post_save, sender=User)
def create_user_profile_and_defaults(sender, instance, created, **kwargs):
    """Ao criar usuário: cria perfil + reserva + categorias + hierarquia de gastos."""
    if not created:
        return

    # 1. Perfil
    Profile.objects.get_or_create(user=instance)

    # 2. Reserva de Emergência
    EmergencyReserve.objects.get_or_create(user=instance)

    # 3. Categorias de Receita
    for cat in DEFAULT_INCOME_CATEGORIES:
        IncomeCategory.objects.get_or_create(user=instance, name=cat['name'], defaults={'icon': cat['icon']})

    # 4. Categorias de Investimento
    for cat in DEFAULT_INVESTMENT_CATEGORIES:
        InvestmentCategory.objects.get_or_create(
            user=instance, name=cat['name'],
            defaults={'investment_type': cat['investment_type'], 'icon': cat['icon']}
        )

    # 5. Hierarquia de Gastos
    for group_data in DEFAULT_EXPENSE_STRUCTURE:
        group, _ = ExpenseGroup.objects.get_or_create(
            user=instance, name=group_data['name'],
            defaults={
                'target_percentage': group_data['target_percentage'],
                'color': group_data['color'],
                'icon': group_data['icon'],
                'order': group_data['order'],
            }
        )
        for sg_data in group_data['subgroups']:
            subgroup, _ = ExpenseSubgroup.objects.get_or_create(
                group=group, name=sg_data['name'],
                defaults={'icon': sg_data['icon']}
            )
            for item_name in sg_data['items']:
                ExpenseItem.objects.get_or_create(subgroup=subgroup, name=item_name)
