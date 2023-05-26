import pytest
from typing import Sequence
from apps.wallet.models import FinancialTransaction
from apps.wallet.logic import summarize_transactions_by_user_email


@pytest.mark.django_db
def test_summarize_transactions_by_user_email(sample_transactions_models: Sequence[FinancialTransaction]) -> None:
    """ Test logic function to aggregate information of total inflow and outflow by user email """

    summarized_queryset = summarize_transactions_by_user_email()
    assert list(summarized_queryset) == [{'user_email': 'janedoe@email.com',
                                          'total_inflow': 2651.4399999999996,
                                          'total_outflow': -761.85},
                                         {'user_email': 'johndoe@email.com',
                                          'total_inflow': 0.0,
                                          'total_outflow': -51.13}]
