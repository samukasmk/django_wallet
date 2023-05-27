from datetime import date

import pytest

from apps.wallet.exceptions import (InflowTransactionHasANegativeAmount,
                                    OutflowTransactionHasAPositiveAmount)
from apps.wallet.models import FinancialTransaction


@pytest.mark.django_db
def test_create_expected_inflow_positive_amount() -> None:
    from apps.wallet.models import FinancialTransaction
    assert FinancialTransaction.objects.all().count() == 0
    FinancialTransaction.objects.create(reference='000001',
                                        date='2021-05-01',
                                        amount=10000.0,
                                        type='inflow',
                                        category='savings',
                                        user_email='john@email.com')
    assert FinancialTransaction.objects.all().count() == 1
    created_transaction = FinancialTransaction.objects.first()
    assert created_transaction.reference == '000001'
    assert created_transaction.date == date(2021, 5, 1)
    assert created_transaction.amount == 10000.0
    assert created_transaction.type == 'inflow'
    assert created_transaction.category == 'savings'
    assert created_transaction.user_email == 'john@email.com'


@pytest.mark.django_db
def test_create_expected_outflow_negative_amount() -> None:
    assert FinancialTransaction.objects.all().count() == 0
    FinancialTransaction.objects.create(reference='000002',
                                        date='2021-05-02',
                                        amount=-20000.0,
                                        type='outflow',
                                        category='house',
                                        user_email='mary@email.com')
    assert FinancialTransaction.objects.all().count() == 1
    created_transaction = FinancialTransaction.objects.first()
    assert created_transaction.reference == '000002'
    assert created_transaction.date == date(2021, 5, 2)
    assert created_transaction.amount == -20000.0
    assert created_transaction.type == 'outflow'
    assert created_transaction.category == 'house'
    assert created_transaction.user_email == 'mary@email.com'


@pytest.mark.django_db
def test_create_unexpected_inflow_negative_amount() -> None:
    assert FinancialTransaction.objects.all().count() == 0
    with pytest.raises(InflowTransactionHasANegativeAmount):
        FinancialTransaction.objects.create(reference='000003',
                                            date='2021-05-03',
                                            amount=-30000.0,
                                            type='inflow',
                                            category='lotery',
                                            user_email='josephine@email.com')
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
def test_create_unexpected_outflow_positive_amount() -> None:
    assert FinancialTransaction.objects.all().count() == 0
    with pytest.raises(OutflowTransactionHasAPositiveAmount):
        FinancialTransaction.objects.create(reference='000004',
                                            date='2021-05-04',
                                            amount=40000.0,
                                            type='outflow',
                                            category='bills',
                                            user_email='leonardo@email.com')
    assert FinancialTransaction.objects.all().count() == 0


@pytest.mark.django_db
def test_model_method_transaction_to_dict() -> None:
    from apps.wallet.models import FinancialTransaction
    assert FinancialTransaction.objects.all().count() == 0
    FinancialTransaction.objects.create(reference='001001',
                                        date='2021-05-01',
                                        amount=10000.0,
                                        type='inflow',
                                        category='savings',
                                        user_email='john@email.com')
    assert FinancialTransaction.objects.all().count() == 1
    created_transaction = FinancialTransaction.objects.first()
    assert created_transaction.to_dict() == dict(reference='001001',
                                                 date='2021-05-01',
                                                 amount='10000.00',
                                                 type='inflow',
                                                 category='savings',
                                                 user_email='john@email.com')


@pytest.mark.django_db
def test_model_method_transaction_to_str() -> None:
    from apps.wallet.models import FinancialTransaction
    assert FinancialTransaction.objects.all().count() == 0
    FinancialTransaction.objects.create(reference='001001',
                                        date='2021-05-01',
                                        amount=10000.0,
                                        type='inflow',
                                        category='savings',
                                        user_email='john@email.com')
    assert FinancialTransaction.objects.all().count() == 1
    created_transaction = FinancialTransaction.objects.first()
    assert str(created_transaction) == str(dict(reference='001001',
                                                date='2021-05-01',
                                                amount='10000.00',
                                                type='inflow',
                                                category='savings',
                                                user_email='john@email.com'))
