from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.wallet.models import FinancialTransaction
from apps.wallet.serializers import FinancialTransactionSerializer


class FinancialTransactionsViewSet(viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer


