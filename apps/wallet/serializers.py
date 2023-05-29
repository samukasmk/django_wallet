from typing import Sequence

from rest_framework import serializers

from apps.wallet.exceptions import (InflowTransactionHasANegativeAmount,
                                    OutflowTransactionHasAPositiveAmount)
from apps.wallet.models import FinancialTransaction
from apps.wallet.validators import validate_amount_signal_for_type


class FinancialTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for LIST and POST actions
    """

    class Meta:
        model = FinancialTransaction
        fields = ['reference', 'date', 'amount', 'type', 'category', 'user_email']

    def validate(self, data: dict) -> dict:
        """
        Validate input values from POST creations
        """
        # check if the value of 'reference' has changed (ignored by patch if 'reference' field is not defined)
        if self.instance and 'reference' in data.keys() and self.instance.reference != data['reference']:
            raise serializers.ValidationError({'reference': ('reference is a read-only field and '
                                                             'it can\'t be changed by payload.')})

        # check signal of amount value before call save method.
        try:
            if 'type' in data.keys() and 'amount' in data.keys():
                validate_amount_signal_for_type(data['type'], float(data['amount']))
        except InflowTransactionHasANegativeAmount as exc:
            raise serializers.ValidationError(
                {'amount': InflowTransactionHasANegativeAmount.message}) from exc
        except OutflowTransactionHasAPositiveAmount as exc:
            raise serializers.ValidationError(
                {'amount': OutflowTransactionHasAPositiveAmount.message}) from exc
        except Exception as exc:
            raise serializers.ValidationError({'unknown': 'error on validation'}) from exc

        # call other validations of inheritance
        return super().validate(data)


class SummaryAllTransactionsByUser(serializers.Serializer):
    """
    Response Serializer for json render of aggregations by user
    """
    user_email = serializers.EmailField()
    total_inflow = serializers.DecimalField(max_digits=None, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=None, decimal_places=2)


class SummaryUserTransactionByCategory(serializers.Serializer):
    """
    Response Serializer for json render of aggregations by user
    """
    inflow = serializers.DictField()
    outflow = serializers.DictField()

    def to_representation(self, queryset_result: Sequence[FinancialTransaction]) -> dict:
        """
        Format QuerySet result into json response
        for dinamic category fields round two places and force to string
        """
        response_dict = {'inflow': {}, 'outflow': {}}
        for summary_category in queryset_result:
            transaction_type = summary_category['type']
            category_name = summary_category['category']
            total_category = summary_category["total"]
            response_dict[transaction_type][category_name] = str(round(total_category, 2))
        return response_dict
