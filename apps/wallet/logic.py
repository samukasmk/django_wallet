from typing import Sequence
from django.db.models import Sum, Q
from apps.wallet.models import FinancialTransaction


def summarize_transactions_by_user_email() -> Sequence[FinancialTransaction]:
    return FinancialTransaction.objects.values(
        'user_email').annotate(total_inflow=Sum('amount',
                                                filter=Q(type='inflow'),
                                                default=0.0),
                               total_outflow=Sum('amount',
                                                 filter=Q(type='outflow'),
                                                 default=0.0))
