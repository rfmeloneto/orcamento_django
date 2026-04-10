"""
Serviço de projeção de despesas recorrentes.

Regras de negócio:
  1. Ao salvar uma Transaction com is_recurring=True, projeta despesas para
     todos os meses seguintes até dezembro do mesmo ano.
  2. Se já existir uma transação projetada (is_projected=True) para aquele
     mês/item, atualiza o valor. Nunca duplica.
  3. Transações reais (is_projected=False) existentes num mês futuro são
     preservadas — servem de nova "fonte da verdade" para os meses seguintes.
  4. Na edição, o novo valor é propagado a partir do mês da transação editada
     em diante, respeitando a regra do item 3.
"""

import datetime
import calendar

from .models import Transaction


def project_recurring(transaction: Transaction) -> int:
    """
    Projeta (cria ou atualiza) despesas recorrentes para os meses futuros
    do mesmo ano, a partir da transação informada.

    Retorna o número de meses projetados/atualizados.
    """
    if not transaction.is_recurring:
        return 0

    source_date = transaction.date
    year        = source_date.year
    start_month = source_date.month + 1  # começa no mês seguinte

    if start_month > 12:
        # Transação lançada em dezembro — nada a projetar no mesmo ano
        return 0

    user        = transaction.user
    item        = transaction.item
    amount      = transaction.amount
    description = transaction.description
    payment     = transaction.payment_method
    notes       = transaction.notes

    projected_count = 0

    for month in range(start_month, 13):
        # Verifica se existe uma transação REAL neste mês (não projetada).
        # Se existir, ela é a nova "fonte da verdade" — paramos aqui.
        real_exists = Transaction.objects.filter(
            user=user,
            item=item,
            date__year=year,
            date__month=month,
            is_projected=False,
            is_recurring=True,
        ).exclude(pk=transaction.pk).exists()

        if real_exists:
            # A partir daqui a projeção é responsabilidade daquela transação real
            break

        # Dia do mês: mantém o mesmo dia ou usa o último dia do mês
        last_day = calendar.monthrange(year, month)[1]
        day      = min(source_date.day, last_day)
        proj_date = datetime.date(year, month, day)

        # Upsert: atualiza projetada existente ou cria nova
        Transaction.objects.update_or_create(
            user=user,
            item=item,
            date__year=year,
            date__month=month,
            is_projected=True,
            defaults={
                'date':           proj_date,
                'amount':         amount,
                'description':    description,
                'payment_method': payment,
                'notes':          notes,
                'is_recurring':   True,
                'is_projected':   True,
            },
        )
        projected_count += 1

    return projected_count


def reproject_from_source(item, user, from_date: datetime.date) -> None:
    """
    Reaplica a projeção a partir de `from_date` usando a transação real mais
    recente como fonte da verdade.

    Útil para recalcular o restante do ano quando uma transação real é
    criada ou editada em meio a um período que já tinha projeções.
    """
    year = from_date.year

    # Busca todas as transações reais recorrentes do item no ano,
    # ordenadas por mês decrescente, para encontrar a mais recente
    # que seja >= from_date.
    real_transactions = (
        Transaction.objects
        .filter(
            user=user,
            item=item,
            date__year=year,
            is_recurring=True,
            is_projected=False,
        )
        .order_by('date__month')
    )

    # Reconstrói a projeção mês a mês a partir de cada transação real,
    # garantindo que uma transação real posterior substitua as projeções.
    for t in real_transactions:
        project_recurring(t)
