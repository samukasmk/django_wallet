from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.wallet.models import FinancialTransaction
from apps.wallet.serializers import FinancialTransactionSerializer, SummaryAllTransactionsByUser, \
    SummaryUserTransactionByCategory
from apps.wallet.logic import summarize_all_transactions_by_user_email, summarize_user_transactions_by_category


class FinancialTransactionsViewSet(viewsets.ModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer

    def list(self, request, *args, **kwargs):
        # return summarized response if action to group_by is declared
        if request.GET.get('group_by') == 'type':
            return self.summary_all_transactions_by_user_email()
        # list all transactions by builtin methods in detail=True
        return super().list(request, *args, **kwargs)

    def summary_all_transactions_by_user_email(self):
        queryset = summarize_all_transactions_by_user_email()
        serializer = SummaryAllTransactionsByUser(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(self, request, *args, **kwargs)
